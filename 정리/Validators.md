## Validators

- django validators와 drf validators가 다르다
- django validators는 model단에서 저장되는 단계에서 check
- drf validators는 serializer로 받는 단계에서 check
  - 따라서 저장하는 단계에서는 확인하지 않는다.
- model에서 `clean` 메서드를 상속받아 save()전 validation 가능



- 자신이 짠 코드를 의심하고, 고민하기
- 더 개선할 수 있는 방법을 고안
- 생각이나 설계를 하지 않으면 고생한다.



- django에서 url path에서 찾을 수 없으면 자동으로 `/`를 붙인다.
- 이것 때문에 rest한 url 구성이 어려우며 설정에서 해제해야 한다.
- 에러처리: 프론트에서 모두 처리

