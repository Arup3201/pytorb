from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Value, CharField, Exists, OuterRef
from django.db.models.functions import Concat
from accounts.models import User
from . import models

def get_project(*, user: User, project_id: str):
    try:
        project = models.Project.objects.annotate(
            is_member=Exists(
                models.Member.objects.filter(
                    project=OuterRef('pk'),
                    user=user
                )
            ),
            is_owner=Exists(
                models.Member.objects.filter(
                    project=OuterRef('pk'),
                    user=user,
                    member_type=models.MemberType.OWNER,
                )
            )
        ).get(id=project_id)
    except models.Project.DoesNotExist:
        return None
    else:
        return project

def get_projects_list(*, user: User, search: str = "", sort: str = "updated", page_number: int = 1):
    projects = models.Project.objects.annotate(
        is_member=Exists(
            models.Member.objects.filter(
                project=OuterRef('pk'),
                user=user
            )
        ),
        is_owner=Exists(
            models.Member.objects.filter(
                project=OuterRef('pk'),
                user=user,
                member_type=models.MemberType.OWNER,
            )
        )
    ).filter(is_member=True)
    if search:
        projects = projects.filter(title__contains = search)

    if not sort:
        sort = "updated"
    if sort == 'title':
        projects = projects.order_by('title')
    elif sort == 'created':
        projects = projects.order_by('-created_at')
    elif sort == 'updated':
        projects = projects.order_by('-updated_at')

    paginator = Paginator(projects, 3)
    page_obj = paginator.get_page(page_number) 

    return page_obj

def create_project(*, title: str, description: str, topics: str, user: User):
    with transaction.atomic():
        project = models.Project.objects.create(title=title, description=description, topics=topics, owner=user)
        models.Member.objects.create(user=user, project=project, member_type=models.MemberType.OWNER)

def edit_project(*, pk: str, title: str, description: str, topics: str):
    project = models.Project.objects.get(pk=pk)
    project.title = title
    project.description = description
    project.topics = topics
    project.save()

def list_members(*, project_id: str, search: str = "", sort: str = "joined", page_number: int = 1):
    members = models.Member.objects.filter(project_id=project_id)
    
    full_name = Concat(
        "user__first_name", 
        Value(" "),
        "user__last_name", 
        output_field=CharField(),
    )
    
    if search:
        members = members.annotate(
            full_name=full_name
        ).filter(full_name__icontains = search)

    if not sort:
        sort = "joined"
    if sort == 'joined':
        members = members.order_by('-created_at')
    elif sort == 'name':
        members = members.annotate(
            full_name=full_name
        ).order_by('full_name')
    elif sort == 'username':
        members = members.order_by('user__username')

    paginator = Paginator(members, 5)
    page_obj = paginator.get_page(page_number)
    
    return page_obj

def get_projects_for_user(*, user: User, search: str = "", sort: str|None = None, page_number: int = 1):
    projects = models.Project.objects.annotate(
        is_member=Exists(
            models.Member.objects.filter(
                project=OuterRef('pk'),
                user=user
            )
        ),
        is_owner=Exists(
            models.Member.objects.filter(
                project=OuterRef('pk'),
                user=user,
                member_type=models.MemberType.OWNER,
            )
        )
    )
    
    if search:
        projects = projects.filter(title__icontains = search.lower())

    if not sort:
        sort = 'created'
    if sort == 'title':
        projects = projects.order_by('title')
    elif sort == 'created':
        projects = projects.order_by('-created_at')
    
    paginator = Paginator(projects, 10)
    page_obj = paginator.get_page(page_number)

    return page_obj

def create_join_request(*, project_id: str, user: User):
    join_request = models.JoinRequest(project_id=project_id, user_id=user.pk)
    join_request.join_status = models.JoinRequestStatus.PENDING
    join_request.save()

def get_join_status(*, project_id: str, user: User):
    try:
        join_request = models.JoinRequest.objects.get(project_id=project_id, user=user)
    except models.JoinRequest.DoesNotExist:
        return ""
    else:
        return join_request.join_status

def list_join_requests(*, project_id: str, search: str = "", sort: str|None = None, page_number: int = 1):
    join_requests = models.JoinRequest.objects.filter(project_id=project_id, join_status=models.JoinRequestStatus.PENDING)

    full_name = Concat(
        "user__first_name", 
        Value(" "),
        "user__last_name", 
        output_field=CharField(),
    )

    if search:
        join_requests = join_requests.annotate(
            full_name=full_name
            ).filter(
                full_name__icontains = search.lower()
                )

    if not sort:
        sort = "requested"
    if sort == 'requested':
        join_requests = join_requests.order_by('-created_at')
    elif sort == 'name':
        join_requests = join_requests.annotate(
            full_name=full_name
        ).order_by('full_name')
    elif sort == 'username':
        join_requests = join_requests.order_by('user__username')

    paginator = Paginator(join_requests, 5)
    page_obj = paginator.get_page(page_number)
    
    return page_obj

def respond_to_join_request(*, project_id: str, requestor_id: str, responder_id: str, response: str):
    with transaction.atomic():
        join_request = models.JoinRequest.objects.get(project_id=project_id, user_id=requestor_id)
        if response=='approve':
            join_request.join_status = models.JoinRequestStatus.ACCEPTED
            models.Member.objects.create(project_id=project_id, user_id=requestor_id)
        elif response=='reject':
            join_request.join_status = models.JoinRequestStatus.REJECTED
    
        join_request.save()
