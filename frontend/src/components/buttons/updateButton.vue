<script setup>
defineProps({
  id: {required: true},
  name: {required: true},
})
</script>

<template>
<router-link class="update" :to="{name: name, params: {id: id}}">Изменить</router-link>
</template>

<style scoped>
.update {
  background-color: #ffe082;
  color: #000000;
  border-radius: 4px;
  padding: 1% 2%;
  font-weight: bold;
  border-style: none;
  text-decoration: none;
  font-size: 14px;
}
</style>