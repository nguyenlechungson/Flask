from app import app,db
from app.models import UserDb,Post



@app.shell_context_processor
def make_shell_context():
    return {'db':db,'UserDb':UserDb,'Post':Post}

if __name__=='__main__':
    app.run(port=5000,debug=False)