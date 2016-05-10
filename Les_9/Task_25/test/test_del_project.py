from model.project import Project
import random


def test_delete_named_project(app):
    project=Project(name="students_project", description="about Project")
    try:
        ind = app.project.get_project_list().index(project)
    except ValueError:
        app.project.create(project)
    old_projects = app.project.get_project_list()
    app.project.delete_named_project(project)
    new_projects = app.project.get_project_list()
    assert len(old_projects) - 1 == len (new_projects)
    old_projects.remove(project)
    assert sorted(old_projects,key=Project.id_or_max) == sorted(new_projects,key=Project.id_or_max)
