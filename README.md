### 플라스크로 게시판 만들기

배웠던 데이터베이스를 이용해서 **게시판 기능을 하는 웹사이트**를 만들어보도록 하자!

1. 메인페이지
   - 타이틀과 내용을 제출할 수 있는 기능을 만든다.
   - 게시판을 조회할 수 있는 버튼을 만든다.
2. create페이지
   - 타이틀과 내용을 이 페이지에서 받아서 **db에 저장**한다.
   - 저장한 다음에는 다시 메인페이지로 redirect한다.
3. 게시판 페이지
   - **10개단위**로 게시물을 보여준다.

```python
from flask import Flask,render_template,request,redirect
import sqlite3
app = Flask(__name__)

@app.route('/') #메인페이지
def index():
    return render_template('index.html')
    
@app.route('/create') #잠깐 들어갔다 나오는 페이지
def create():
    c = sqlite3.connect('board.sqlite3')
    db = c.cursor()
    title = request.args.get('title')
    content = request.args.get('content')
    db.execute("INSERT INTO articles (title,content) VALUES (?,?)",(title,content))
    c.commit()
    c.close()
    return redirect("/")
    
@app.route('/page/<int:num>') #게시판 페이지
def page(num):
    c = sqlite3.connect('board.sqlite3')
    db = c.cursor()
    sql_read = "SELECT * FROM articles LIMIT 10 OFFSET ?"
    res = db.execute(sql_read,(10*num,)).fetchall()
    c.close()
    return render_template('page.html',res=res)
```

- 메인페이지

```html
<!-- index.html -->
<div class="container" style="background-color:rgb(18,18,18,0.5);">
    <!-- 입력기능 만들기 -->
    <div class="row">
        <div class="col-4 d-flex align-items-center" 
             style="font-weight:700; font-size:50px; color:#fff">
            게시판<br>
            입니다
        </div>
        <div class="col-4 d-flex justify-content-center">
            <form action="/create">
                <input type="text" class="d-block" style="background-color:#fff;"
                       name="title" placeholder="제목을 입력해 주세요"/>
                <input type="text" style="height:400px; background-color:#fff;"
                       name="content" placeholder="내용을 입력해 주세요"/>
                <input type="submit" value="Submit"/>
            </form>
        </div>
        <div class="col-2"></div>
    </div>
    <!-- 게시판으로 가는 버튼 만들기 -->
    <div class="row d-flex justify-content-center">
        {% for idx in range(10) %}
        <button><a href="/page/{{idx}}">{{idx}}</a></button>
        {% endfor %}
    </div>
</div>
```

![1](https://user-images.githubusercontent.com/37765338/52032524-a6636580-2564-11e9-8df9-d13ed492a85d.png)

- create 페이지는 어자피 redirect하기 위한 용도이므로 html을 구성하지 않았음.

  (url에서 지정된 인자를 가져오기위함)

- 게시판 페이지

```html
<div class="container">
    <!-- 게시글을 보여주는 기능 -->
    <div class="row">
        <div class="col-1 border border-info">id</div>
        <div class="col-3 border border-info">제목</div>
        <div class="col-8 border border-info">내용</div>
    </div>
    {% for r in res %}
    <div class="row">
        <div class="col-1 border border-info">{{r[0]}}</div>
        <div class="col-3 border border-info">{{r[1]}}</div>
        <div class="col-8 border border-info">{{r[2]}}</div>
    </div>
    {% endfor %}
	<!-- 홈페이지로 돌아가는 기능 -->
    <form action="/">
        <input type="submit" value="홈페이지로 돌아가기"/>
    </form>
</div>
```

![2](https://user-images.githubusercontent.com/37765338/52032526-a6fbfc00-2564-11e9-97a4-fff6a06eeef8.png)

이렇게 구성하면 메인페이지에서 입력한 제목과 내용이 그대로 **디비에 저장**이 되서 각 게시판의 링크마다 10개씩 뿌려준다.

<br>

### 게시글 삭제하기

그런데 의문점이 하나 생긴다.

1편에서 **DB의 장점은 삭제와 수정이 용이하다**고 했는데 그 부분이 구현이 안되어있다.

**특정 글에 삭제버튼을 누르면 글이 지워지는 기능**을 만들어보자.

아이디어는 간단하다.

1. 삭제버튼을 만든다.

2. 삭제버튼을 누르면 delete링크로 보낸다.

   (단 삭제할 글을 구별할 수 있게 **/delete/게시물id/게시판num** 의 형식으로 보내야한다. )

3. delete링크에서 해당하는 글을 삭제하고 다시 해당하는 게시판으로 redirect한다.

(단! type을 신중하게 정해야한다. **return값은 무조건 string**이므로 num이 숫자여도 string으로 받아야함)

<br>

```python
@app.route('/delete/<int:id_>/<num>')
def delete(id_,num):
    c = sqlite3.connect('board.sqlite3')
    db = c.cursor()
    db.execute('DELETE FROM articles WHERE id = ?',(id_,))
    c.commit()
    return redirect('/page/'+num)
```

```html
<div class="col-2">
    <button><a href="/delete/{{r[0]}}/{{num}}">삭제</a></button>
</div>
<!-- num은 게시판 번호이고, r[0]은 id입니다 -->
```

여기서 6번글 삭제버튼을 누르면,

![3](https://user-images.githubusercontent.com/37765338/52032527-a6fbfc00-2564-11e9-8f8a-7ddc70242d9f.png)

이런 식으로 글이 없어지는 것을 확인할 수 있다.

![4](https://user-images.githubusercontent.com/37765338/52032529-a7949280-2564-11e9-89ba-944b77077582.png)

<br>

### 게시글 수정

글을 수정하는건 삭제하는거보다 구현이 더 어려운데,

왜냐하면 수정을 위해서는 수정하기위한 페이지를 만들어줘야하기 때문이다.

(예시: 깃허브)

![5](https://user-images.githubusercontent.com/37765338/52032530-a7949280-2564-11e9-8b00-41866540dcd1.png)

이런것처럼 수정버튼을 누르면 수정할 수 있는 페이지로 이동하기때문.

로직은 간단하다.

1. 각 글마다 **수정버튼**을 만든다 + **/edit으로 이동**

   ```html
   <button><a href="/edit/{{r[0]}}/{{num}}">수정</a></button>
   ```

   예를 들어서, 0번게시판의 2번째글을 수정하는 버튼을 누르면

   /edit/2/0 으로 이동할 수 있다.

   ![6](https://user-images.githubusercontent.com/37765338/52032531-a7949280-2564-11e9-97d7-2893231803a9.png)

   <br>

2. **/edit에서 글을 수정**해서 제출버튼을 누르면 **/edit_result**로 수정정보를 보낸다.

   ```python
   @app.route('/edit/<int:id_>/<num>')
   def edit(id_,num):
       c = sqlite3.connect('board.sqlite3')
       db = c.cursor()
       contents = db.execute('SELECT title,content FROM articles WHERE id = ?',(id_,)).fetchone()
       return render_template('edit.html',contents=contents,id_=id_,num=num)
   ```

   ```html
   <!-- edit.html -->
   <div class="container" style="background-color:rgb(18,18,18,0.5);">
       <div class="row">
           <div class="col-4 d-flex align-items-center" 
                style="font-weight:700; font-size:50px; color:#fff">
               글 수정<br>
               하세요
           </div>
           <div class="col-4 d-flex justify-content-center">
               <form action="/edit_result">
                   <input type="text" class="d-block" style="background-color:#fff;" name="title" value="{{contents[0]}}"/>
                   <input type="text" style="height:400px; background-color:#fff;" name="content" value="{{contents[1]}}"/>
                   <input type="hidden" name="id" value="{{id_}}">
                   <input type="hidden" name="num" value="{{num}}">
                   <input type="submit" value="Submit"/>
               </form>
           </div>
           <div class="col-2"></div>
       </div>
   </div>
   ```

   어자피 입력받는 form이랑 유사하게 하는게 가장 편하므로 index.html을 적극 활용한다.

   그러나, 수정하려면 원래 글과 제목이 보존되어있어야하므로 form태그의 value속성을 이용해서 기본값을 지정해준다. (placeholder과는 다름)

   수정할 id와 게시판 넘버는 변하지 않으나, /edit_result 로 보내야하는 값이므로 hidden타입을 이용해서 보내준다.

   ![7](https://user-images.githubusercontent.com/37765338/52032528-a6fbfc00-2564-11e9-9811-265fdc220a81.png)

   글을 수정하고 제출해보자.

   <br>

3. **/edit_result**에서 글을 수정해주고 원래 게시판으로 redirect를 한다.

   ```python
   @app.route('/edit_result')
   def edit_result():
       c = sqlite3.connect('board.sqlite3')
       title = request.args.get('title')
       content = request.args.get('content')
       id_ = request.args.get('id')
       num = request.args.get('num')
       db = c.cursor()
       sql_update = "UPDATE articles SET title = ?,content = ? WHERE id = ?"
       db.execute(sql_update,(title,content,id_))
       c.commit()
       return redirect('/page/'+num)
   ```

   글을 수정해주고 원래 게시판으로 redirect 해준 결과를 볼 수 있다.

   ![8](https://user-images.githubusercontent.com/37765338/52032532-a82d2900-2564-11e9-92af-b8b3e5e82438.png)

물론 POST로 하지 않고 GET방식으로 전부 구현하였으나, 실제로는 POST방식을 사용해야한다.

그리고 1번의 a태그의 링크가 보이는 것을 막기 위해서 자바스크립트를 이용하여 링크정보를 json파일로도 보낼수 있다고 합니다. 

<br>

나중에는 이러한 기능뿐만 아니라 댓글기능이나 로그인기능같은 다양한 기능들이 추가되고, 데이터가 쌓이면서 복잡해지는데 이러한 기능들의 관계를 잘 정의해주는 것이 중요하다.

<br>
