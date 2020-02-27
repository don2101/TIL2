### Service

- 여러 코드에서 반복적으로 사용되는 코드 분리
- 지연 초기화: 의존성으로 주입하기 전 까지 초기화가 되지 않는다.
- 싱글턴: 하나의 인스턴스만 생성하여 각 컴포넌트에서 하나의 인스턴스 참조



Service와 Factory는 유사하지만 명확히 다르다

- Angular 코드에서 Service는 Factory를 사용하여 구현된다.



Service

- 주입해서 사용할 수 있고, new 키워드를 통해 인스턴스 초기화도 가능
- public method나 변수를 제공하기 위해 사용

```javascript
// Service 정의
function SomeService() {
	this.testing = 1;
	this.testing2 = 2;

	this.tempMethod = function(saySomething) {
		console.log(saySomething);
	}

}

let service_main1 = angular.module("service_main1", []);
service_main1.service("service1", SomeService); // Service 등록

// Service를 주입해서 사용
let main = angular.module("main", ["service_main1"]); // 모듈 주입

main.controller("main_test", function($scope, service1) { // 서비스 주입
	console.log(service1.testing); // 1
	console.log(service1.testing2); // 2
	console.log(service1.tempMethod); // function에 관련한 
	service1.tempMethod("Good day"); // Good day

	service1.testing = 4;
	service1.testing2 = 5;
});

main.controller("main_test2", function($scope, service1){
    // 싱글턴 생성이기 때문에 main_test와 동일한 service1을 공유
	console.log(service1.testing); // 4
	console.log(service1.testing2); // 5
});

// Service 주입 없이 new 키워드를 통해 사용
let main = angular.module("main", []);

main.controller("main_test", function($scope) {
	let service1 = new SomeService();
	console.log(service1.testing);
	console.log(service1.testing2);
	console.log(service1.tempMethod);
	service1.tempMethod("Good day");
    // ... 위와 동일한 출력
});
```







Factory

- 비즈니스 로직 또는 모듈 제공자로 사용
- 객체나 클로저를 반환해야 외부에서 사용 가능
- 노출식 모듈 패턴

https://edykim.com/ko/post/revealing-module-pattern/

https://webclub.tistory.com/5

```javascript
// factory 정의
function someFactory() {
	let private_variable = 1;
	let public_variable = 2;

	let module_method = function(say) {
		console.log(say);
	};

	let get_private_variable = function() {
		return private_variable;
	}

	return {
		return_method: module_method,
		get_private_variable: get_private_variable,
		public_var: public_variable,
	}
}

let factory_module = angular.module("factory", []);
factory_module.factory("factory", someFactory); // factory 등록


let main_module = angular.module("main_module", ["factory"]); // factory 주입

main_module.controller("main_cont", function($scope, factory) {
	console.log(factory.private_variable); // undefined
	console.log(factory.public_var); // 2
	factory.return_method("good day"); // good day
	console.log(factory.get_private_variable()); // 1
	factory.public_var += 1;
	console.log(factory.public_var); // 3
});
```





노출식 모듈 패턴

- 일부 메서드 및 변수를 외부에서 사용할 수 없도록 지정할 수 있다.

```javascript
let module_test = (function(window) {
	let hey = window;
	let temp = function(hey) {
		console.log(hey);
	}

	return {
		h: temp
	}
})("sdf");


let d = module_test
d.h('sdf');
```





- 서비스는 초기화 과정이 존재하기 때문에 prototype 상속 가능
  - 일반적으로 상속이 필요한 경우에 서비스로 구현
  - helper나 정적 메서드 활용에는 팩토리로 구현