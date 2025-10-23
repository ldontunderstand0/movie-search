<script setup>
defineProps({
  name: {required: true},
})
</script>

<template>
<router-link class="update" :to="{name: name}">Создать</router-link>
</template>

<style scoped>
.update {
  background-color: #45dc2e;
  color: #ffffff;
  border-radius: 4px;
  padding: 1% 2%;
  font-weight: bold;
  border-style: none;
  text-decoration: none;
  font-size: 14px;
}
</style>