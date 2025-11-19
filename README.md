## 🚀 AWS EC2 2대 + NGINX 로드밸런싱 + GitHub Actions 자동 배포

### 📌 Overview

- EC2 2대 운영 & NGINX 로드밸런싱 적용
- GitHub Actions 자동 배포 파이프라인 구축
- 서버별 환경 변수 분리 및 동시 배포 처리

---

## 🧱 인프라 구성도

<p align="center">
  <img width="755" height="542" src="https://github.com/user-attachments/assets/da4d0e6d-9746-4372-a684-621431b4b224" alt="image" />
</p>



---

## 🔧 GitHub Actions 설정

### ✅ 1. Secrets 설정

| Key | Description |
|-----|---------------|
| EC2_USER | EC2 접속 유저 |
| EC2_KEY | PEM Key 내용 전체 |
| EC2_HOST1 |서버 #1 IP |
| EC2_HOST2 | 서버 #2 IP |
| EC2_HOST | Nginx Reverse Proxy Server |
|AWS_ACCESS_KEY_ID|  IAM 액세스 키 |
|AWS_REGION|  aws 지역명 |
|AWS_S3_BUCKET|  aws s3 버킷 이름 |
|AWS_SECRET_ACCESS_KEY| IAM 시크릿 키 |
|GMAIL_PASSWORD| Gmail 2차 비밀번호 |
|GMAIL_USER| Gmail 보내는 사람 이메일 |
|JWT_SECRET| openssl rand -base64 32의 결과 값 |
|KAKAO_CLIENT_ID| 카카오 rest api 키 |
|KAKAO_CLIENT_SECRET| 카카오 secret 키 |
|NAVER_CLIENT_ID| 네이버 Client ID |
|NAVER_CLIENT_SECRET| 네이버 Client Secret |
|SMS_ACCESS_KEY| coolsms access 키 |
|SMS_SECRET_KEY| coolsms secret 키 |



---

### ⚙️ 2. Workflow 파일 및 Dockerfile 파일 생성하기

| 파일 | 설명 | 링크 |
|------|--------|--------|
|`load_balancing_deploy.yml`| GitHub Actions 배포 설정| 🔗 [보기](https://github.com/alzkdpf000/actions-load-balancing-app/blob/master/.github/workflows/load_balancing_deploy.yml)|
|`Dockerfile`| Docker 빌드 설정| 📦 [보기](https://github.com/alzkdpf000/actions-load-balancing-app/blob/master/Dockerfile)|



## 🌐 NGINX Load Balancer 설정

### 1. 설치
```bash
# 설치 명령어
 sudo apt install -y nginx

 # 상태 확인
 sudo systemctl status nginx
 

```
### 2. 설정 파일 생성
```bash
# 파일 만들기 [이름은 자유롭게]
 sudo vim /etc/nginx/sites-available/[이름] 
```
### 3. 설정 작성
```nginx
upstream [이름] {
        least_conn;
        server <EC2-IP-1>:80;
        server <EC2-IP-2>:80;
}

server {
        listen 80;

        location / {
                proxy_pass http://[이름];
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
        }
}
```

### 4. 적용 및 검증
```bash
# 기존 링크 삭제하기
sudo rm /etc/nginx/sites-enabled/default

# 만든 파일 링크 걸어주기
sudo ln -s /etc/nginx/sites-available/[이름] /etc/nginx/sites-enabled/

# 확인하기
ls -l /etc/nginx/sites-enabled/

# 설정한 파일에 문제 있는지 체크
sudo nginx -t
```
### 5. 결과
![](https://velog.velcdn.com/images/alzkdpf000/post/2bc26a19-32bc-40c3-be4c-97f3b1b46cf9/image.png)


## ⚖️ 로드 밸런싱 알고리즘 비교
| 알고리즘                  | 설명                 | 추천 사용 사례                |
| --------------------- | ------------------ | ----------------------- |
| **Round Robin(Default)**       | 순차 분배              | 서버 스펙이 모두 동일할 때         |
| **Weighted RR**       | 가중치 기반 분배          | 서버 성능이 다를 때             |
| **Least Connections** | 연결 수가 가장 적은 서버에 분배 | API 요청 길이가 긴 서비스        |
| **IP Hash**           | 동일 사용자 요청 → 동일 서버  | 세션 공유 어려울 때 (Redis 미사용) |
| **Hash**              | 쿠키/헤더 기반 라우팅       | A/B 테스트, 특정 사용자 고정 라우팅  |

---
# 🤖 AI 감정 분석 기능

## 📌 기능 개요
사용자가 작성한 **일기/문장**을 분석하여 감정을 분류하는 기능이다.  
FastAPI 서버에서 **Multinomial Naive Bayes(나이브 베이즈)** 모델을 사용해 감정 결과를 반환한다.

## 🧠 베이즈 추론, 베이즈 정리, 베이즈 추정 (Bayesian Inference)
- 역확률(inverse probability) 문제를 해결하기 위한 방법으로서, 조건부 확률(P(B|A)))을 알고 있을 때, 정반대인 조건부 확률(P(A|B))을 구하는 방법이다.
- 추론 대상의 사전 확률과 추가적인 정보를 기반으로 해당 대상의 "사후 확률"을 추론하는 통계적 방법이다.
- 어떤 사건이 서로 "배반"하는(독립하는) 원인 둘에 의해 일어난다고 하면, 실제 사건이 일어났을 때 이 사건이 두 원인 중 하나일 확률을 구하는 방식이다.
- 어떤 상황에서 N개의 원인이 있을 때, 실제 사건이 발생하면 N개 중 한 가지 원인일 확률을 구하는 방법이다.
- 기존 사건들의 확률을 알 수 없을 때, 전혀 사용할 수 없는 방식이다.
- 하지만, 그 간 데이터가 쌓이면서, 기존 사건들의 확률을 대략적으로 뽑아낼 수 있게 되었다.
- 이로 인해, 사회적 통계나 주식에서 베이즈 정리 활용이 필수로 꼽히고 있다. 

## ⚡ 사용 이유

### ✅ 나이브 베이즈 분류 (Naive Bayes Classifier)
- 텍스트 분류를 위해 전통적으로 널리 사용되는 분류기로서, 짧은 문장 분류에 특히 강점을 보인다.
- 베이즈 정리에 기반한 통계적 기법으로, 정확도 대비 연산 비용이 매우 낮고, 대용량 데이터에서도 빠르게 동작한다.
- 모든 feature가 서로 독립적이라고 가정하는 **조건부 독립 가정(naive assumption)**을 기반으로 한다.
- 감정 분석, 스팸 필터링, 문서 분류, 추천 시스템 등 다양한 NLP 서비스에서 활용된 전통적 모델이다.
- 실 데이터에서 모든 feature가 완전히 독립적인 경우는 거의 없지만, 그럼에도 불구하고 텍스트 기반 문제에서는 놀라울 만큼 안정적인 성능을 보이는 장점이 있다.

## 📚 사용 데이터셋

모델 학습은 아래의 한국어 감정 데이터셋을 기반으로 진행했다.

| 데이터셋명 | 설명 | 출처 |
|-----------|------|------|
| **한국어 감정 텍스트 데이터** | 감성 카테고리가 정리된 텍스트 데이터 | 🔗 [https://aihub.or.kr](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&dataSetSn=263) |



## 🔧 모델 설명

### ✔️ 알고리즘  
- **Multinomial Naive Bayes**  
  - 텍스트 분류에 특화  
  - 단어 등장 빈도 기반으로 감정 라벨 예측  

### ✔️ 전처리 & 학습 과정
1. 특수문자 제거 / 형태소 단위 정규화(kiwipiepy 사용)
2. `CountVectorizer` 로 BoW(단어 출현 빈도) 벡터 변환
3. MultinomialNB 학습
4. `feeling_model.pkl` 로 모델 저장 후 FastAPI에 로드

#### 🔗 [모델 훈련 코드](https://github.com/alzkdpf000/study-machine-learning/blob/master/b_classifier/feeling.ipynb)

## ⚙️ FastAPI 감정 분석 엔드포인트

```python
@app.post("/api/feel-check", response_model=FeelingCheckResponse)
async def check_spam(request: FeelingCheckRequest):
    print(request.message)
    model = joblib.load("feeling_model.pkl")

    # 감정 예측
    prediction = model.predict([request.message])[0]

    return {"result": str(prediction)}
```

<img width="475" height="151" alt="image" src="https://github.com/user-attachments/assets/89ba525e-5645-4d7c-b19e-d48dfdba5408" />


---

## 🎨 프론트엔드 활용

- 감정 결과에 따라  
  - **아이콘 이미지 표시**  
  - **감정 색상 테마**  
  - **일기 상세뷰에 감정 이미지 추가**  

<img width="624" height="432" alt="image" src="https://github.com/user-attachments/assets/e5378d56-ee0a-4610-b1b5-39af333597df" />

---

## 🎯 사용 예시

| 입력 예시 | 예측 감정 |
|-----------|-----------|
| "아무렇지 않은 척했지만, 사실 오늘은 많이 화가 났다." | 화남 |
| "아무 이유 없이 웃음이 나는 날도 있는 법이다." | 기쁨 |
| "손끝까지 전해지는 떨림을 숨길 수 없었다." | 무서움 |
| "설명할 수 없지만, 묘하게 마음에 들지 않는 하루였다." | 싫음 |
| "잠깐의 충격이지만, 심장이 세 번은 더 뛰었다." | 놀람 |
| "따뜻한 바람처럼 고요함이 마음을 스쳐 지나갔다." | 평화로움 |
| "이유는 모르지만 눈물이 고이던 그런 순간이 있었다." | 슬픔 |


---

## 🧩 Troubleshooting

### 1.
| Issue                  | Cause               |
| ---------------------- | ------------------- |
| NGINX Welcome Page 표시됨 | 설정 미적용           |

![](https://velog.velcdn.com/images/alzkdpf000/post/c26765e9-e4d5-4509-8a60-3ed9aca75152/image.png)

### 1.1 해결
<code>sudo systemctl reload nginx</code>
<code>sudo systemctl status nginx </code>
<code>sudo nginx -t</code>를 실행하고 success가 나온 것을 한 번 더 확인하고 실행하니 잘 동작하였다.

<br>

### 2.
| Issue                  | Cause               | 
| ---------------------- | ------------------- | 
| SSH Deploy Error       | PEM Key or HOST 미변경 |

![](https://velog.velcdn.com/images/alzkdpf000/post/8b4b3dff-812a-4338-89f5-4fa9a7a4a2d2/image.png)

### 2.1 해결
actions를 설정할 때 pem키와 $HOST로 안 바꾼 부분 때문에 아래와 같은 오류가 발생했습니다.


### 3.
| Issue                  | Cause               | 
| ---------------------- | ------------------- | 
| 정확도가 너무 낮음       | 데이터의 질이 낮다고 판단 |


<img width="426" height="106" alt="스크린샷 2025-11-18 오후 4 53 52" src="https://github.com/user-attachments/assets/d4881675-3abb-41c8-a4e2-ee3b15349ec4" />


### 3.1 해결
<br>
[https://raw.githubusercontent.com](https://raw.githubusercontent.com/ohgzone/file1/main/aihub_coupus.csv) 대신 다른 데이터를 찾아 해결했습니다.


### 4.
| Issue                  | Cause               | 
| ---------------------- | ------------------- | 
| 실제 데이터 판단 시 낮은 성능을 보이는 것 같음     | 훈련 데이터처럼 조사를 없애지 않고 예측 진행 |


<img width="859" height="72" alt="스크린샷 2025-11-18 오후 4 49 20" src="https://github.com/user-attachments/assets/b246ad83-6428-46ef-b13a-cd23576c28c9" />


### 4.1 해결
<img width="696" height="130" alt="스크린샷 2025-11-18 오후 4 49 31" src="https://github.com/user-attachments/assets/656a6a82-2b76-4c06-9bbb-eb5b935ef4ef" />
<br>실제 데이터에서도 조사를 없애주고 예측을 진행했습니다.

### 5.
| Issue                  | Cause               | 
| ---------------------- | ------------------- | 
| 성능을 높여보기   | 사전 확률을 맞추지 않고 실행 |


<img width="421" height="107" alt="스크린샷 2025-11-18 오후 5 01 52" src="https://github.com/user-attachments/assets/9e08804f-6ffc-4079-b374-a1dbfa7665a3" />



### 5.1 해결

<img width="834" height="200" alt="image" src="https://github.com/user-attachments/assets/160a5429-948f-4e24-8d0a-0ffea62109b3" />

- **나이브 베이즈(Naive Bayes)**는 **사전 확률(P(Class))**과 **조건부 확률(P(Feature|Class))**을 기반으로 예측을 수행한다.
- 예측 과정에서 각 클래스(라벨)의 사전 확률은 전체 데이터에서 해당 클래스가 차지하는 비율로 계산된다.
- 만약 특정 클래스의 데이터가 매우 적으면, 그 클래스의 사전 확률이 낮게 계산되어 모델이 해당 클래스를 과소평가하게 된다.
- 반대로 클래스별 데이터가 균등하면, 모든 클래스가 동일하게 고려되므로, 조건부 확률 계산이 편향되지 않고 안정적인 예측이 가능하다.

<img width="475" height="151" alt="스크린샷 2025-11-18 오후 4 16 06" src="https://github.com/user-attachments/assets/8268040f-eb2b-4f68-b554-a7c8577ff329" />
<br>약소하지만 그래도 성능이 향상되었다.

--- 


