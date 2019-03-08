from sklearn.preprocessing import LabelEncoder, OneHotEncoder

label_enc = LabelEncoder()
values = ['cat', 'dog', 'cat']
label_enc.fit(values)
integer_encoded = label_enc.fit_transform(values)
print(integer_encoded)

onehot_encoder = OneHotEncoder(sparse=False, categories='auto')
integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
print(integer_encoded)
onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
print(onehot_encoded)

print(onehot_encoder.inverse_transform(onehot_encoded))