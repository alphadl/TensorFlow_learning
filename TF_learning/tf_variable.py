import tensorflow as tf

stat=tf.Variable(0,name='counter')
# print stat.name
one=tf.constant(1)

new_value=tf.add(stat,one)
updata=tf.assign(stat,new_value)

init=tf.initialize_all_variables() #must hava if define variable

with tf.Session() as sess:
    sess.run(init)
    for _ in range(3):
        sess.run(updata)
        print sess.run(stat)
