from datetime import datetime
import json
from app.extensions import db

class Analysis(db.Model):
    __tablename__ = 'analyses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    data_source_id = db.Column(db.Integer, db.ForeignKey('data_sources.id'))
    name = db.Column(db.String(100), nullable=False)
    analysis_type = db.Column(db.String(50), nullable=False)  # elasticity, promo_analysis, forecast
    parameters = db.Column(db.Text)  # JSON с параметрами анализа
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, running, completed, failed
    schedule = db.Column(db.String(100))  # CRON выражение для регулярного запуска
    last_run = db.Column(db.DateTime)
    next_run = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Отношения
    company = db.relationship('Company', backref='analyses')
    results = db.relationship('AnalysisResult', backref='analysis', lazy='dynamic')
    
    @property
    def params(self):
        if self.parameters:
            return json.loads(self.parameters)
        return {}
    
    @params.setter
    def params(self, params_dict):
        self.parameters = json.dumps(params_dict)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'company_id': self.company_id,
            'data_source_id': self.data_source_id,
            'name': self.name,
            'analysis_type': self.analysis_type,
            'parameters': self.params,
            'status': self.status,
            'schedule': self.schedule,
            'last_run': self.last_run.isoformat() if self.last_run else None,
            'next_run': self.next_run.isoformat() if self.next_run else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class AnalysisResult(db.Model):
    __tablename__ = 'analysis_results'
    
    id = db.Column(db.Integer, primary_key=True)
    analysis_id = db.Column(db.Integer, db.ForeignKey('analyses.id'))
    result_data = db.Column(db.Text)  # JSON с результатами
    summary = db.Column(db.Text)  # Текстовое резюме (возможно от OpenAI)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def results(self):
        if self.result_data:
            return json.loads(self.result_data)
        return {}
    
    @results.setter
    def results(self, results_dict):
        self.result_data = json.dumps(results_dict)
    
    def to_dict(self):
        return {
            'id': self.id,
            'analysis_id': self.analysis_id,
            'results': self.results,
            'summary': self.summary,
            'created_at': self.created_at.isoformat()
        }