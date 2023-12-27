<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import axios from 'axios';

const todos = ref([])
const name = ref('');
const input_content = ref('');
const input_category = ref(null);

const todos_asc = computed(() => todos.value.sort((a, b) => {
  return b.createdAt - a.createdAt
}))

// edit this to talk to azure function!!!!
const addTodo = () => {
  if (input_content.value.trim() === '' || input_category.value === null) {
    return
  }

  axios.post('api/addTodo',{
      category: input_category.value,
      content: input_content.value,
      createdAt: new Date().getTime(),
      done: false
      })
      .then(res => {
          todos.value = res.data
          console.log('Added item to python arr via post call:')
      })
      .catch(error => {
          console.error('Error:', error);
      });

  input_content.value = ''
  input_category.value = null
}

const removeTodo = todo => {
  axios.post('api/removeTodo',todo)
      .then(res => {
          todos.value = res.data
          console.log('Removed item from python arr via post call:')
      })
      .catch(error => {
          console.error('Error:', error);
      });
}

const updateName = newName => {
  console.log('new name: ' + newName)
  axios.post('api/setName',{name: newName})
      .then(res => {
          console.log('res data updated name')
          console.log(res.data.name)
          name.value = res.data.name
          console.log('Updated name from python arr via post call:')
      })
      .catch(error => {
          console.error('Error:', error);
      });
}

// pulls name on  mount
onMounted(() => {
  axios.get('api/getName')
            .then(res => {
                console.log('Your name')
                console.log(res.data.name)
                name.value = res.data.name
            })
            .catch(error => {
                console.error('Error:', error);
            });

  axios.get('api/getTodos')
            .then(res => {
                console.log('hopefully a list is outputted below')
                console.log(res.data)
                todos.value = res.data;
            })
            .catch(error => {
                console.error('Error:', error);
            });
})
</script>

<template>
  <main class="app">
    <section class="greeting">
      <h2 class="title">
        What's up, <input type="text" placeholder="Name here" v-model="name">
        <button class="updateName" @click="updateName(name)">Save name</button>
      </h2>
    </section>

    <section class="create-todo">
      <h3>Create a todo</h3>
      <form @submit.prevent="addTodo">
        <input 
            type="text"
            placeholder="e.g. make a video"
            v-model = "input_content">

        <h4>Pick a category</h4>
        <div class="options">
          <label>
            <input 
                type="radio"
                name="category"
                value="business"
                v-model="input_category">
                <span class="bubble business"></span>
                <div>Business</div>
          </label>
          <label>
            <input 
                type="radio"
                name="category"
                value="personal"
                v-model="input_category">
                <span class="bubble personal"></span>
                <div>Personal</div>
          </label>
        </div>

        <input type="submit" value="Add todo">
      </form>
    </section>

    <section class="todo-list">
      <h3>TODO LIST</h3>
      <div class="list">
        <div v-for="todo in todos_asc" :class="`todo-item ${todo.done && 'done'}`">
          <label>
            <input type="checkbox" v-model="todo.done">
            <span :class="`bubble ${todo.category}`"></span>
          </label>
          <div class="todo-content">
            <input type="text" v-model="todo.content">
          </div>
          <div class="actions">
            <button class="delete" @click="removeTodo(todo)">Delete</button>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>