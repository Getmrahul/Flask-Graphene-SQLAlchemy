import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from database import db_session,User as UserModel
from sqlalchemy import and_

class Users(SQLAlchemyObjectType):
	class Meta:
	    model = UserModel
	    interfaces = (relay.Node, )

# Used to Create New User
class createUser(graphene.Mutation):
	class Input:
		name = graphene.String()
		email = graphene.String()
		username = graphene.String()
	ok = graphene.Boolean()
	user = graphene.Field(Users)

	@classmethod
	def mutate(cls, _, args, context, info):
		user = UserModel(name=args.get('name'), email=args.get('email'), username=args.get('username'))
		db_session.add(user)
		db_session.commit()
		ok = True
		return createUser(user=user, ok=ok)
# Used to Change Username with Email
class changeUsername(graphene.Mutation):
	class Input:
		username = graphene.String()
		email = graphene.String()

	ok = graphene.Boolean()
	user = graphene.Field(Users)

	@classmethod
	def mutate(cls, _, args, context, info):
		query = Users.get_query(context)
		email = args.get('email')
		username = args.get('username')
		user = query.filter(UserModel.email == email).first()
		user.username = username
		db_session.commit()
		ok = True

		return changeUsername(user=user, ok = ok)


class Query(graphene.ObjectType):
	node = relay.Node.Field()
	user = SQLAlchemyConnectionField(Users)
	find_user = graphene.Field(lambda: Users, username = graphene.String())
	all_users = SQLAlchemyConnectionField(Users)

	def resolve_find_user(self,args,context,info):
		query = Users.get_query(context)
		username = args.get('username')
		# you can also use and_ with filter() eg: filter(and_(param1, param2)).first()
		return query.filter(UserModel.username == username).first()


class MyMutations(graphene.ObjectType):
	create_user = createUser.Field()
	change_username = changeUsername.Field()

schema = graphene.Schema(query=Query, mutation=MyMutations, types=[Users])
