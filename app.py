from flask import Flask,render_template,request,redirect,session,url_for,send_from_directory
import os,json

app=Flask(__name__)
app.secret_key="minitube_secret"

UPLOAD_FOLDER="uploads"
USER_FILE="users.json"

os.makedirs(UPLOAD_FOLDER,exist_ok=True)

def load_users():
    with open(USER_FILE) as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE,"w") as f:
        json.dump(users,f)

@app.route("/")
def login_page():
    return render_template("login.html")

@app.route("/login",methods=["POST"])
def login():

    username=request.form["username"]
    password=request.form["password"]

    users=load_users()

    if username in users and users[username]==password:
        session["user"]=username
        return redirect("/home")

    return redirect("/")

@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route("/register_user",methods=["POST"])
def register_user():

    username=request.form["username"]
    password=request.form["password"]

    users=load_users()
    users[username]=password
    save_users(users)

    return redirect("/")

@app.route("/home")
def home():

    if "user" not in session:
        return redirect("/")

    videos=os.listdir(UPLOAD_FOLDER)

    return render_template(
        "home.html",
        username=session["user"],
        videos=videos
    )

@app.route("/upload",methods=["GET","POST"])
def upload():

    if request.method=="POST":

        file=request.files["video"]

        if file:
            file.save(os.path.join(UPLOAD_FOLDER,file.filename))

        return redirect("/home")

    return render_template("upload.html")

@app.route("/video/<filename>")
def video(filename):
    return render_template("video.html",filename=filename)

@app.route("/delete/<filename>")
def delete(filename):

    if "user" not in session:
        return redirect("/")

    file_path = os.path.join("uploads", filename)

    if os.path.exists(file_path):
        os.remove(file_path)

    return redirect("/home")

@app.route("/uploads/<filename>")
def uploaded(filename):
    return send_from_directory(UPLOAD_FOLDER,filename)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__=="__main__":
    port=int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)
