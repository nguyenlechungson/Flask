from app import create_app,db
from app.models import UserDb,Post

#tạo biến toàn cục app từ hàm create_app
app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db':db,'UserDb':UserDb,'Post':Post}

if __name__=='__main__':
    app.run(debug=True)