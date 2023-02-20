from flask import Flask, Response, make_response, request


class FlaskExercise:
    """
    Вы должны создать API для обработки CRUD запросов.
    В данной задаче все пользователи хранятся в одном словаре, где ключ - это имя пользователя,
    а значение - его параметры. {"user1": {"age": 33}, "user2": {"age": 20}}
    Словарь (dict) хранить в памяти, он должен быть пустым при старте flask.

    POST /user - создание пользователя.
    В теле запроса приходит JSON в формате {"name": <имя пользователя>}.
    Ответ должен вернуться так же в JSON в формате {"data": "User <имя пользователя> is created!"}
    со статусом 201.
    Если в теле запроса не было ключа "name", то в ответ возвращается JSON
    {"errors": {"name": "This field is required"}} со статусом 422

    GET /user/<name> - чтение пользователя
    В ответе должен вернуться JSON {"data": "My name is <name>"}. Статус 200

    PATCH /user/<name> - обновление пользователя
    В теле запроса приходит JSON в формате {"name": <new_name>}.
    В ответе должен вернуться JSON {"data": "My name is <new_name>"}. Статус 200

    DELETE /user/<name> - удаление пользователя
    В ответ должен вернуться статус 204
    """

    @staticmethod
    def configure_routes(app: Flask) -> None:
        DB: dict = {}

        def update_db_dict(old_name: str, new_name: str) -> None:
            new_user_dict = {new_name: value for key, value in DB.items() if key == old_name}
            DB.pop(old_name)
            DB.update(new_user_dict)
            return None

        @app.post("/user")
        def create_user() -> Response:
            data = request.get_json()
            user_name = data.get("name", None)

            if user_name is None:
                response = make_response({"errors": {"name": "This field is required"}}, 422)
                return response

            DB[user_name] = {}
            response = make_response({"data": f"User {user_name} is created!"}, 201)
            return response

        @app.get("/user/<name>")
        def get_user(name: str) -> Response:
            if DB.get(name, None) is None:
                response = make_response(
                    {"errors": {"name": "There are no user with this name"}}, 404
                )
                return response

            response = make_response({"data": f"My name is {name}"}, 200)
            return response

        @app.patch("/user/<name>")
        def update_user(name: str) -> Response:
            new_user_name = request.get_json()["name"]

            update_db_dict(name, new_user_name)

            response = make_response({"data": f"My name is {new_user_name}"}, 200)
            return response
