import graphene
from graphene_django import DjangoObjectType

from characters.models import Character, Vote
from users.schema import UserType
from graphql import GraphQLError


class CharacterType(DjangoObjectType):
    class Meta:
        model = Character

# Add after the CharacterType
class VoteType(DjangoObjectType):
    class Meta:
        model = Vote

class Query(graphene.ObjectType):
    characters = graphene.List(CharacterType)
    votes = graphene.List(VoteType)

    def resolve_characters(self, info, **kwargs):
        return Character.objects.all()

    def resolve_votes(self, info, **kwargs):
        return Vote.objects.all()

class CreateCharacter(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    image = graphene.String()
    genre = graphene.String()
    species = graphene.String()
    status =  graphene.String()
    
    posted_by = graphene.Field(UserType)

    class Arguments:
        name = graphene.String()
        image = graphene.String()
        genre = graphene.String()
        species = graphene.String()
        status =  graphene.String()
        
    def mutate(self, info, name,image,genre,species,status):
        user = info.context.user or None

        character = Character( 
                    name=name, 
                    image=image,
                    genre=genre,
                    species=species,
                    status=status,
                    posted_by = user
                   )
        character.save()

        return CreateCharacter(
            id=character.id,
            name=character.name,
            image=character.image,
            genre=character.genre,
            species=character.species,
            status=character.status,
            posted_by=character.posted_by,
        )


# Add the CreateVote mutation

class CreateVote(graphene.Mutation):
    user = graphene.Field(UserType)
    character = graphene.Field(CharacterType)

    class Arguments:
        character_id = graphene.Int()

    def mutate(self, info, character_id):
        user = info.context.user
        if user.is_anonymous:
            #raise Exception('You must be logged to vote!')
            raise GraphQLError('GraphQLError: You must be logged to vote!')


        character = Character.objects.filter(id=character_id).first()
        if not character:
            raise Exception('Invalid Character!')

        Vote.objects.create(
            user=user,
            character=character,
        )

        return CreateVote(user=user, character=character)




class Mutation(graphene.ObjectType):
    create_character = CreateCharacter.Field()
    create_vote = CreateVote.Field()
