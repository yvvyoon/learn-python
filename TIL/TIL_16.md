# Flask framework

## File-Uploads

[Flask 공식 문서][http://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/#uploading-files]에서 파일 업로드 관련 예제를 따라해보다가 계속 되는 에러와 실패를 마주해 크나큰 슬픔에 빠져 있을 때였다. 맨 밑에 `An Easier Solution`이라고 눈에 띄는 소제목이 있었는데 무려 파일 업로드 익스텐션이 있다는 꿀정보다.

네이티브하게 로직을 구현하는 것이 궁극적인 목표지만 일단 제대로 구현이라도 해봐야 대충 로직을 파악할 수 있을 거라고 합리화하며 `Flask-Uploads` 익스텐션을 사용해보기로 했다. 언어, 프레임워크에 구애받지 않고 파일 업로드 로직은 어느 애플리케이션에나 동일한데 아직 와닿지 않는다.

<br>

## 파일 업로드

<br>

> *https://www.roytuts.com/ajax-files-upload-using-python-flask-jquery/*

<br>

## 파일 다운로드

<br>

> https://www.roytuts.com/how-to-download-file-using-python-flask/

<br>

AJAX로 파일을 업로드하고, 등록 버튼을 클릭하여 글 등록을 완료하는 시점에 첨부파는 파일의 이름을 데이터베이스로 insert하는 로직을 구현하고 있다. 처음에는 `routes.py` 파일 안에 전역변수로 파일명을 두고, 첨부파일 업로드할 때 파일 이름 저장, 저장된 그 파일명을 `register_article()` 메소드에서 재사용하여 데이터베이스에 넣고 있었는데, 전역변수이다보니 할당된 값이 소멸되지 않고 그대로 남아 있어 파일을 첨부하지 않은 채 글을 등록해도 직전에 업로드했던 파일이 동일하게 첨부되는 현상이 발생했다.

전역변수를 데이터베이스 커밋 직후에 초기화하려고 했는데 애초에 전역변수를 사용하지 않는 방법으로 리팩토링하고자 한다. 글을 등록하는 로직을 클래스화해서 구현해보자.

<br>

```python
@app.route('/article/upload', methods=['POST'], endpoint='upload_file')
def upload_file():
    if 'files[]' not in request.files:
        response = jsonify({'message': '요청에 파일 관련 정보가 없습니다.'})
        response.status_code = 400

        return response

    files = request.files.getlist('files[]')

    errors = {}
    success = False

    for file in files:
        if file and allowed_file(file.filename):
            # secure_filename() 메소드를 사용하면 한글이 사라짐
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_DIRECTORY'], filename))
            success = True

            # 전역변수를 사용하려면 선언할 때 global 예약어를 주는 게 아니라
            # 사용할 함수 스코프 내에서 global 예약어를 붙여서 별도로 한 번 더 선언해줘야 한다.
            global uploaded_filename
            uploaded_filename = filename

            # logger.info(f'업로드된 파일명: {uploaded_filename}')
        else:
            success = False

            errors[file.filename] = '허용되지 않은 확장자입니다.'

    if success and errors:
        response = jsonify({'message': '파일이 성공적으로 업로드되었습니다.'})
        response.status_code = 206

        return response

    if success:
        response = jsonify({'message': '파일이 성공적으로 업로드되었습니다.'})
        response.status_code = 201

        return response
    else:
        response = jsonify(errors)
        response.status_code = 400

        return response
```

<br>

해킹을 방지하기 위해 `secure_filename()` 메소드를 통해 파일명을 한번 변경 후 업로드하게 된다. 그런데 이 메소드를 통과하는 순간 한글이 사라지는 현상이 발생했다. 구글링을 해보니 일본어도 마찬가지인 모양이다.

