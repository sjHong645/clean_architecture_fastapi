from ulid import ULID
from datetime import datetime
from user.domain.user import User
from user.domain.repository.user_repo import IUserRepository
from user.infra.repository.user_repo import UserRepository
from utils.crypto import Crypto

from fastapi import HTTPException


class UserService: 

    def __init__(self) : 

        self.user_repo : IUserRepository = UserRepository() 
        self.ulid = ULID()

        self.cryto = Crypto()

    def create_user(self, name : str, email : str, password : str) : 

        #### 중복 유저가 있는지 확인하는 부분 ####
        _user = None # 1번

        try : 
            _user = self.user_repo.find_by_email(email)
        except HTTPException as e :
            if e.status_code != 404 : 
                raise e
            
        if _user is not None : # 2번 
            raise HTTPException(status_code=422)

        #### 유저를 저장하는 부분 ####
        now = datetime.now()
        
        user : User = User(
            id = self.ulid.generate(),
            name = name,
            email = email,
            # password = password,
            password = self.cryto.encrypt(password),
            created_at = now,
            updated_at = now
        )

        self.user_repo.save(user)

        return user
    