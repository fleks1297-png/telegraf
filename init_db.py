from app import app, db

with app.app_context():
    # Удаляем всё (если есть)
    db.drop_all()
    # Создаём заново
    db.create_all()
    print("✅ База данных и таблицы созданы!")
    
    # Проверяем
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    print("Таблицы в БД:", inspector.get_table_names())
