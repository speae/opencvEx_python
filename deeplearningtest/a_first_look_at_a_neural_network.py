from tensorflow import keras
import matplotlib.pyplot as plt
import random
from keras import models
from keras import layers
from tensorflow.keras.utils import to_categorical

print(keras.__version__)

Dataset = 'mnist'
# Dataset = 'fashion_mnist'

# 사람 손글씨 데이터셋 숫자 0 ~ 9
# STEP 1. 데이터셋 가져오기
if Dataset == 'fashion_mnist':
    from tensorflow.keras.datasets import fashion_mnist

    #  첫 번째 tuple에는 train데이터셋, 두번째 튜플에는 test 데이터셋
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
else:
    from tensorflow.keras.datasets import mnist

    (train_images, train_labels), (test_images, test_labels) = mnist.load_data()

# 이미지 장 수, 이미지 높이, 이미지 폭
print(train_images.shape)

# 이미지의 레이블(정답)의 개수; 이미지가 6만장이면 정답도 6만개
print(len(train_labels))

print(train_labels)
print(train_labels[:10])

print(test_images.shape)
print(len(test_labels))

# train 데이터셋에서 랜덤하게 이미지를 선택하고, 레이블값도 함께 출력
num = random.randint(0, 60000)
print(num, train_labels[num])
digit = train_images[num]

plt.imshow(digit, cmap=plt.cm.binary)
plt.show()

#  STEP 2. 모델 생성(정의)
# 딥러닝을 위한 모델을 생성하는데 add하는 방식 ->
# 레이어를 쌓는 방식으로 모델을 구성하겠다는 의미
# 모델을 다시 생성하면 가중치 초기화
network = models.Sequential()

# 입력 레이어           히든 레이어의 개수
network.add(layers.Dense(512, activation='relu', input_shape=(28 * 28,)))

# 출력 레이어
network.add(layers.Dense(10, activation='softmax'))

# STEP 3. 옵티마이저(경사하강법을 어떤 것으로 사용할지 정의), 손실함수, 측정 기준 정의
network.compile(optimizer='rmsprop',
                loss='categorical_crossentropy',
                metrics=['accuracy'])

# MINST의 픽셀값이 0~255 사이의 정수로 되어있는 것 확인
print(train_images[0])

print(train_images.shape)

# STEP 4. 데이터 전처리 : 3차원 -> 2차원 차수변경(Deep Neural Network에서 이미지를 1차원으로 변경(이미지 장수 제외))
train_images = train_images.reshape((60000, 28 * 28))

print(train_images.shape)

# 정규화(Normalization) : 픽셀값을 0~1 사이의 실수(float32)숫자로 변경 -> 데이터의 정확도를 높일 수 있음
train_images = train_images.astype('float32') / 255

test_images = test_images.reshape((10000, 28 * 28))
test_images = test_images.astype('float32') / 255

print(train_labels[:3])

# one-hot encoding(원 핫 엔코딩)
# keras에서 one-hot encoding으로 변경시켜주는 API
train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)

# overfitting(과대적합)을 확인하려면(=몇 epoch만에 overfitting이 발생하는지 확인하려면)
# train데이터셋에서 validation 데이터셋을 나누어주자.
# train 데이터셋이 6만장 => train 데이터셋 49980장, validation 데이터셋 1만장
from sklearn.model_selection import train_test_split
# 1st : X 데이터, train 이미지
# 2nd : Y 데이터, train 레이블
# 3rd : 데이터셋을 나누는 비율; train:validation의 비율
# 4th : random_state는 random seed값;
# random seed값을 고정하는 이유 : optimizer나 epoch을 변동했을 때 데이터셋을 shuffle하므로
# 데이터셋이 어떻게 구성되느냐에 대해 영향을 받지 않기 위함
# X_train, X_valid, y_train, y_valid = train_test_split(train_images, train_labels, test_size=0.167, random_state=42)
# X_train.shape, X_valid.shape

# STEP 5. 학습
# 모델 -> 컴파일 -> 학습도 가능
# x => 정규화를 시킨 실수 픽셀값을 갖는 이미지
# y => one-hot encoding으로 변환된 레이블
# epochs => train 데이터셋이 6만장인데 6만장의 이미지를 모두 한번씩 참조하면 1 epoch
# batch_size => 한번의 경사하강법을 진행할 때(Loss값을 구할 때 몇 장의 이미지를 사용할 지)
# step_per_epoch => 469 반올림 필요(60000/128)
# verbose : 모드
# validation_split : train_test_split() 메소드의 test_size의 값과 비슷한 역할
history = network.fit(x=train_images, y=train_labels, epochs=40, batch_size=128, validation_split=0.167)

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(len(acc))

plt.plot(epochs, acc, 'bo', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.legend()

plt.figure()

plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()

plt.show()