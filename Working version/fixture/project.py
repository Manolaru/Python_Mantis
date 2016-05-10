from model.project import Project


class ProjectHelper:
   def __init__(self,app):
        self.app = app

   project_cache = None

   def open_manage_projects_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("/manage_proj_page.php")):
            wd.find_element_by_link_text("Manage").click()
            wd.find_element_by_link_text("Manage Projects").click()


   def create(self, project):
        wd = self.app.wd
        self.open_manage_projects_page()
        # init project creation
        wd.find_element_by_css_selector("td.form-title > form > input.button-small").click()
        self.fill_project_form(project)
        # submit project creation
        wd.find_element_by_css_selector("input.button").click()
        self.project_cache = None

   def  delete_named_project(self, project):
        wd = self.app.wd
        self.open_manage_projects_page()
        wd.find_element_by_link_text(project.name).click()
        wd.find_element_by_css_selector("form > input.button").click()
        wd.find_element_by_css_selector("input.button").click()
        self.project_cache = None

   def fill_project_form(self, project):
       # fill project form
       wd = self.app.wd
       self.change_field_value("name", project.name)
       self.change_field_value("description", project.description)

   def change_field_value(self, field_name, text):
       wd = self.app.wd
       if text is not None:
          wd.find_element_by_name(field_name).click()
          wd.find_element_by_name(field_name).clear()
          wd.find_element_by_name(field_name).send_keys(text)

   def get_project_list(self):
       if self.project_cache is None:
           wd = self.app.wd
           self.open_manage_projects_page()
           self.project_cache =[]
           rows = wd.find_elements_by_class_name("row-1") + wd.find_elements_by_class_name("row-2")
           for row in rows:
               columns = row.find_elements_by_css_selector("td")
               if len(columns) == 5:
                   project_name = columns[0].text
                   idstring = columns[0].find_element_by_css_selector("a").get_attribute("href")
                   id = idstring[idstring.find('project_id=')+len('project_id='):]
                   description = columns[4].text
                   self.project_cache.append(Project(name=project_name, id=id, description=description))
       return list(self.project_cache)



