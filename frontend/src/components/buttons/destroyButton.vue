<script setup>
defineProps({
  id: {required: true},
  api: {required: true},
})
const destroy = async (id, api) => {
  await api.destroy(id)
  window.location.reload()
}
</script>

<template>
<button class="destroy" @click="destroy(id, api)">Удалить</button>
</template>

<style scoped>
.destroy {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  font-size: 14px;
  background-color: #ffacac;
  color: #000000;
  border-radius: 4px;
  padding: 1% 2%;
  font-weight: bold;
  border-style: none;
  cursor: pointer
}
</style>