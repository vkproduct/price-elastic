from datetime import datetime
from app import db

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    plan_type = db.Column(db.String(20), nullable=False)  # free, standard, business, enterprise
    status = db.Column(db.String(20), nullable=False)  # active, cancelled, expired
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Отношения
    company = db.relationship('Company', backref='subscription', uselist=False)
    payments = db.relationship('Payment', backref='subscription', lazy='dynamic')
    
    def is_active(self):
        return self.status == 'active' and (self.end_date is None or self.end_date > datetime.utcnow())
    
    def to_dict(self):
        return {
            'id': self.id,
            'company_id': self.company_id,
            'plan_type': self.plan_type,
            'status': self.status,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'is_active': self.is_active(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscriptions.id'))
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), nullable=False, default='USD')
    payment_method = db.Column(db.String(50))
    transaction_id = db.Column(db.String(100))
    status = db.Column(db.String(20), nullable=False)  # completed, pending, failed
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'subscription_id': self.subscription_id,
            'amount': self.amount,
            'currency': self.currency,
            'payment_method': self.payment_method,
            'transaction_id': self.transaction_id,
            'status': self.status,
            'payment_date': self.payment_date.isoformat(),
            'created_at': self.created_at.isoformat()
        }