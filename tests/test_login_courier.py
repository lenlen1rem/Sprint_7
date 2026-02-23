import pytest
import allure
from generators import generate_fake_courier
from methods.courier_methods import CourierMethods
from data import Message, TestData

@allure.feature('Логин курьера')
class TestLoginCourier:

    @allure.title('Успешная авторизация курьера')
    def test_login_courier_success(self, create_and_delete_courier):
        login, password = create_and_delete_courier

        with allure.step('Отправить POST-запрос на авторизацию курьера'):
            response = CourierMethods.login_courier(login, password)

        with allure.step('Проверить статус-код 200'):
            assert response.status_code == 200

        with allure.step('Проверить, что ответ содержит id курьера'):
            response_data = response.json()
            assert 'id' in response_data
            assert isinstance(response_data['id'], int)

    @allure.title('Ошибка при авторизации без логина')
    def test_login_without_login(self):
        with allure.step('Отправить POST-запрос на авторизацию без логина'):
            response = CourierMethods.login_courier('', 'valid_password')

        with allure.step('Проверить статус-код 400'):
            assert response.status_code == 400

        with allure.step('Проверить сообщение об ошибке'):
            response_data = response.json()
            assert 'message' in response_data
            assert response_data['message'] == Message.LOGIN_COURIER_MISSING_FIELDS

    @allure.title('Ошибка при авторизации без пароля')
    def test_login_without_password(self):
        with allure.step('Отправить POST-запрос на авторизацию без пароля'):
            response = CourierMethods.login_courier('valid_login', '')

        with allure.step('Проверить статус-код 400'):
            assert response.status_code == 400

        with allure.step('Проверить сообщение об ошибке'):
            response_data = response.json()
            assert 'message' in response_data
            assert response_data['message'] == Message.LOGIN_COURIER_MISSING_FIELDS

    @allure.title('Ошибка при авторизации с несуществующим логином')
    def test_login_with_nonexistent_login(self, create_and_delete_courier):
        _, password = create_and_delete_courier

        with allure.step('Отправить POST-запрос на авторизацию с несуществующим логином'):
            response = CourierMethods.login_courier(TestData.NONEXISTENT_LOGIN, password)

        with allure.step('Проверить статус-код 404'):
            assert response.status_code == 404

        with allure.step('Проверить сообщение об ошибке'):
            response_data = response.json()
            assert 'message' in response_data
            assert response_data['message'] == Message.LOGIN_COURIER_NOT_FOUND

    @allure.title('Ошибка при авторизации с несуществующим паролем')
    def test_login_with_invalid_password(self, create_and_delete_courier):
        login, _ = create_and_delete_courier

        with allure.step('Отправить POST-запрос на авторизацию с несуществующим паролем'):
            response = CourierMethods.login_courier(login, TestData.NONEXISTENT_PASSWORD)

        with allure.step('Проверить статус-код 404'):
            assert response.status_code == 404

        with allure.step('Проверить сообщение об ошибке'):
            response_data = response.json()
            assert 'message' in response_data
            assert response_data['message'] == Message.LOGIN_COURIER_NOT_FOUND
