import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np
import matplotlib.pyplot as plt
import joblib

# CSV 파일 로드
data = pd.read_csv('battery_data.csv')

# 특성 (volt) 및 타겟 변수 (time) 추출
X = data[['volt']]
y = data['time']

# 데이터를 훈련 및 테스트 세트로 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 선형 회귀 모델 생성
model = LinearRegression()

# 모델 훈련
model.fit(X_train, y_train)

# 훈련된 모델을 파일로 저장
joblib.dump(model, 'battery_model.joblib')

# 파일에서 모델 로드
loaded_model = joblib.load('battery_model.joblib')

# 테스트 세트에 대한 예측 수행
y_pred = loaded_model.predict(X_test)

def format_minutes_to_hours_and_minutes(minutes):
    hours = minutes // 60
    remaining_minutes = minutes % 60
    formatted_time = f"{int(hours):02d}시간 {int(remaining_minutes):02d}분"
    return formatted_time

# 모델 평가
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# 임의의 배터리 잔량으로 테스트
new_volt_values = np.array([0.9, 1.1, 1.3]).reshape(-1, 1)  
predicted_time = loaded_model.predict(new_volt_values)
# 예측 결과 표시
for volt, time in zip(new_volt_values.flatten(), predicted_time):
    print(f'Volt: {volt}, Predicted Time: {format_minutes_to_hours_and_minutes(time)}')
# 훈련 데이터 플로팅
plt.scatter(X_train, y_train, color='blue', label='Training Data')
# 테스트 데이터 플로팅
plt.scatter(X_test, y_test, color='red', label='Testing Data')
# 회귀 선 플로팅
plt.plot(X_test, y_pred, color='black', linewidth=3, label='Regression Line')
# 예측된 값 플로팅
plt.scatter(new_volt_values, predicted_time, color='green', marker='*', s=200, label='Predicted Values')
# 레이블 및 제목 추가
plt.xlabel('Volt')
plt.ylabel('Time')
plt.title('Linear Regression Model')
plt.legend()
plt.show()
