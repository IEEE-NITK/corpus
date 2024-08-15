import json
from django.core.management.base import BaseCommand, CommandParser
from blog.models import Post,Tag
from accounts.models import ExecutiveMember,User
from datetime import datetime

class Command(BaseCommand):
    help = "to migrate authors from the json file to the User model"

    def add_arguments(self,parser):
        parser.add_argument('json_file',type=str,help='Path to the json file')

    def handle(self,*args,**kwargs):
        json_file = kwargs['json_file']

        with open(json_file,'r') as file:
            data = json.load(file)

            counter=0
            for post in data:
                name_arr = post['author_name'].split()
                first_name = name_arr[0]
                last_name = name_arr[-1]
                tags = Tag.objects.filter(tag_name=post['categories'][0])
                author = ExecutiveMember.objects.filter(user__first_name=first_name,user__last_name=last_name)[0]
                layout = post["layout"]
                title = post["title"]
                slug=post["slug"]
                description = post["description"]
                author_github = post["github_username"]
                text = post["text"]
                published_date =  datetime.strptime(post["date"], "%Y-%m-%dT%H:%M:%S")
                blog_post = Post(layout=layout,title=title,author=author,slug=slug,description=description,author_github=author_github,text=text,published_date=published_date)
                blog_post.save()
                blog_post.blog_tag.set(tags)
                print(counter)
                counter = counter+1






