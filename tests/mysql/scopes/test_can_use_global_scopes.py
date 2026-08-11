import unittest

from src.masoniteorm.models import Model
from src.masoniteorm.scopes import (
    SoftDeletesMixin,
)


class UserSoft(Model, SoftDeletesMixin):
    __dry__ = True


class User(Model):
    __dry__ = True


class TestMySQLGlobalScopes(unittest.TestCase):
    def test_can_use_global_scopes_on_select(self):
        expected_sql = "SELECT * FROM `user_softs` WHERE `user_softs`.`name` = 'joe' AND `user_softs`.`deleted_at` IS NULL"
        query_sql = UserSoft.where("name", "joe").to_sql()
        self.assertEqual(query_sql, expected_sql)

    def test_can_use_global_scopes_on_time(self):
        expected_sql = "INSERT INTO `users` (`users`.`name`, `users`.`created_at`, `users`.`updated_at`) VALUES ('Joe'"
        query_sql = User.create({"name": "Joe"}, query=True).to_sql()
        self.assertTrue(query_sql.startswith(expected_sql))
