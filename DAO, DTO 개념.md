## DTO vs DAO

### 1. DAO

- Data Access Object
- Database의 data에 접근하기 위한 객체



#### connection pool

- DB에 접근하기 위해서 매번 connection 객체를 생성해야 한다.
- connection pool은 이러한 connection 객체를 미리 생성하여 보관하는 저장소
- 필요할 때 마다 connection 객체를 사용 후 반납



> ##### 그러나...

- 웹 서비스에서 행위가 많아질 수록 여러번의 connection이 발생
- connection pool이 connection을 또 만드는 오버헤드 발생...
- connection을 효율적으로 하기 위해 **DB에 접근하는 객체**를 생성하고, 모든 페이지에서 해당 객체를 사용하게 한다.



#### DAO

- DAO는 이렇게 connection 하나를 통해 DB에 접근하는 객체
- DB를 사용해 데이터를 조회하거나 저장하는 기능을 전담하는 객체
- 사용자는 자신이 필요한 interface를 DAO에 던지고, DAO는 이 interface를 구현한 객체를 사용자에게 제공



### 2. Data Transfer Object(=Value Obejct)

- 계층간 데이터 교환을 위한 Java beans
- 계층간이라는 의미는 DB - Controller간 데이터 교환을 의미하며, DTO는 이러한 계층간 데이터 교환에 사용
- VO는 DTO와 동일한 속성이지만, read only(select의 경우)에 사용



#### 특징

- 로직을 갖지 않는 순수한 데이터 객체
- 속성과 속성에 접근하기 위한 getter, setter 메서드만 가진 클래스



> #### 사용자의 요청과 DAO, VO 간의 연결

![](https://user-images.githubusercontent.com/19590371/78569133-1b63b680-785e-11ea-8577-668886d2347a.png)













