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

  todos.value.push({
    content: input_content.value,
    category: input_category.value,
    done: false,
    createdAt: new Date().getTime()
  })

  input_content.value = ''
  input_category.value = null
}

const removeTodo = todo => {
  todos.value = todos.value.filter(t => t !== todo)
}

watch(todos, newVal => {
  localStorage.setItem('todos', JSON.stringify(newVal))
}, { deep: true })

// changes name
watch(name, (newVal) => {
  localStorage.setItem('name', newVal);
})

// pulls name on  mount
onMounted(() => {
  name.value = localStorage.getItem('name') || ''
  todos.value = JSON.parse(localStorage.getItem('todos')) || []

  axios.get('api/getData')
            .then(res => {
                console.log('Your name')
                console.log(res.data)
                name.value = res.data
            })
            .catch(error => {
                console.error('Error:', error);
            });

  axios.get('api/getData?value=list')
            .then(res => {
                console.log('hopefully a list is outputted below')
                console.log(res.data)
                todos.value = res.data;
            })
            .catch(error => {
                console.error('Error:', error);
            });

  axios.post('api/addTodo',{
              category: "personal",
              content: "test message 1",
              createdAt: 1703632030060,
              done: false
            })
            .then(res => {
                console.log('trying a post request. output is below:')
                console.log(res.data)
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