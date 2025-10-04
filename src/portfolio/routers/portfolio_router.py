class PortfolioRouter:
    portfolio_users_database = "portfolio"
    default_database = "default"

    def read(self, model):
        if model._meta.model_name == "portfolio":
            return self.portfolio_users_database
        else:
            return None

    def write(self, model):
        if model._meta.model_name == "portfolio":
            return self.portfolio_users_database
        else:
            return None

    def migrate(self, database, app_label, model=None):
        if model == "user" or model == "comment":
            return database == "portfolio"
        else:
            return database == "default"
