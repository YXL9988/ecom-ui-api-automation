from .dashboard import DashboardPage


class LoginPage:
    def __init__(self,page):
        self.page = page


    def navigate(self,app_url):
        self.page.goto(app_url)

    def login(self,userEmail,password):
        self.page.get_by_placeholder("email@example.com").fill(userEmail)
        self.page.get_by_placeholder("enter your passsword").fill(password)
        self.page.get_by_role("button", name="Login").click()
        dashboardPage = DashboardPage(self.page)
        return dashboardPage
