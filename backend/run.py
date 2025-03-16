from app import create_app, db
from app.models import User, Company, Subscription, DataSource, Analysis, AnalysisResult

app = create_app()

# Контекст оболочки Flask
@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Company': Company,
        'Subscription': Subscription,
        'DataSource': DataSource,
        'Analysis': Analysis,
        'AnalysisResult': AnalysisResult
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True) 