import graphene
from graphene_django.types import DjangoObjectType
from .models import Task

class TaskType(DjangoObjectType):
    class Meta:
        model = Task

class Query(graphene.ObjectType):
    all_tasks = graphene.List(TaskType, is_completed=graphene.Boolean(required=False))
    task = graphene.Field(TaskType, id=graphene.Int(required=True))

    def resolve_all_tasks(root, info, is_completed=None):
        if is_completed is not None:
            return Task.objects.filter(is_completed=is_completed)
        return Task.objects.all()

    def resolve_task(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Task.objects.get(pk=id)

        return None

# Define mutations here
class TaskInput(graphene.InputObjectType):
    title = graphene.String()
    description = graphene.String()
    is_completed = graphene.Boolean()

class CreateTask(graphene.Mutation):
    class Arguments:
        input = TaskInput(required=True)

    task = graphene.Field(TaskType)

    @staticmethod
    def mutate(root, info, input=None):
        task = Task(
            title=input.title,
            description=input.description,
            is_completed=input.is_completed if input.is_completed is not None else False
        )
        task.save()
        return CreateTask(task=task)

class UpdateTask(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        description = graphene.String()
        is_completed = graphene.Boolean()

    task = graphene.Field(TaskType)

    @classmethod
    def mutate(cls, root, info, id, title=None, description=None, is_completed=None):
        task = Task.objects.get(pk=id)
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if is_completed is not None:
            task.is_completed = is_completed
        task.save()
        return UpdateTask(task=task)

class DeleteTask(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        task = Task.objects.get(pk=id)
        task.delete()
        return DeleteTask(success=True)

# Add to class Query
class Mutation(graphene.ObjectType):
    create_task = CreateTask.Field()
    update_task = UpdateTask.Field()
    delete_task = DeleteTask.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)