from datetime import datetime
import json
from app import db

class DataSource(db.Model):
    __tablename__ = 'data_sources'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    name = db.Column(db.String(100), nullable=False)
    source_type = db.Column(db.String(50), nullable=False)  # file, google_sheets, manual
    file_path = db.Column(db.String(255))  # Для файловых источников
    google_sheet_id = db.Column(db.String(255))  # Для Google Sheets
    column_mapping = db.Column(db.Text)  # JSON с маппингом колонок
    row_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_sync = db.Column(db.DateTime)
    
    # Отношения
    company = db.relationship('Company', backref='data_sources')
    analyses = db.relationship('Analysis', backref='data_source', lazy='dynamic')
    
    @property
    def mapping(self):
        if self.column_mapping:
            return json.loads(self.column_mapping)
        return {}
    
    @mapping.setter
    def mapping(self, mapping_dict):
        self.column_mapping = json.dumps(mapping_dict)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'company_id': self.company_id,
            'name': self.name,
            'source_type': self.source_type,
            'file_path': self.file_path,
            'google_sheet_id': self.google_sheet_id,
            'column_mapping': self.mapping,
            'row_count': self.row_count,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'last_sync': self.last_sync.isoformat() if self.last_sync else None
        }