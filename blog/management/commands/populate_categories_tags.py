"""
Management command to populate default categories and tags.
Run: python manage.py populate_categories_tags
"""
from django.core.management.base import BaseCommand
from blog.models import Category, Tag


class Command(BaseCommand):
    help = 'Populates the database with default categories and tags'

    def handle(self, *args, **options):
        # Default Categories
        categories = [
            'Technology',
            'Programming',
            'Web Development',
            'Mobile Development',
            'Data Science',
            'Artificial Intelligence',
            'Machine Learning',
            'Design',
            'UI/UX',
            'Business',
            'Marketing',
            'Finance',
            'Health & Fitness',
            'Lifestyle',
            'Travel',
            'Food & Cooking',
            'Education',
            'Science',
            'History',
            'Entertainment',
            'Sports',
            'Music',
            'Photography',
            'Art & Culture',
            'News',
            'Opinion',
            'Tutorials',
            'Reviews',
            'Tips & Tricks',
            'Personal Development',
        ]

        # Default Tags
        tags = [
            'Python',
            'Django',
            'JavaScript',
            'React',
            'Vue.js',
            'Node.js',
            'HTML',
            'CSS',
            'Bootstrap',
            'Tailwind CSS',
            'TypeScript',
            'Angular',
            'Flutter',
            'Swift',
            'Kotlin',
            'Java',
            'C++',
            'C#',
            'PHP',
            'Ruby',
            'Go',
            'Rust',
            'SQL',
            'MongoDB',
            'PostgreSQL',
            'MySQL',
            'Redis',
            'Docker',
            'Kubernetes',
            'AWS',
            'Azure',
            'Git',
            'GitHub',
            'CI/CD',
            'API',
            'REST',
            'GraphQL',
            'Microservices',
            'DevOps',
            'Agile',
            'Scrum',
            'Startup',
            'Entrepreneurship',
            'Productivity',
            'Remote Work',
            'Career',
            'Freelancing',
            'Tutorial',
            'Beginner',
            'Advanced',
            'Best Practices',
            'Code Review',
            'Testing',
            'Security',
            'Performance',
            'Optimization',
            'Frontend',
            'Backend',
            'Full Stack',
            'Mobile',
            'Web',
            'Desktop',
            'Cloud',
            'Serverless',
            'Blockchain',
            'Cryptocurrency',
            'NFT',
            'Web3',
            'Metaverse',
            'VR',
            'AR',
            'IoT',
            'Automation',
            'Open Source',
            'Community',
            'Learning',
            'Resources',
            'Tools',
            'Frameworks',
            'Libraries',
            'Tips',
            'Tricks',
            'Hacks',
            'News',
            'Updates',
            'Trends',
            'Future',
            'Innovation',
        ]

        # Create Categories
        created_categories = 0
        for category_name in categories:
            category, created = Category.objects.get_or_create(name=category_name)
            if created:
                created_categories += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created category: {category_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Category already exists: {category_name}'))

        # Create Tags
        created_tags = 0
        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            if created:
                created_tags += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created tag: {tag_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Tag already exists: {tag_name}'))

        self.stdout.write(self.style.SUCCESS(
            f'\n✓ Successfully created {created_categories} new categories and {created_tags} new tags!'
        ))
        self.stdout.write(self.style.SUCCESS(
            f'Total: {Category.objects.count()} categories, {Tag.objects.count()} tags'
        ))

