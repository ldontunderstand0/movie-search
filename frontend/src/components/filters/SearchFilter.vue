<script setup>
defineProps({
  search: {
    type: String,
    required: true
  },
  placeholder: {
    type: String,
    required: true
  }
})
</script>

<template>
<div class="filter-group">
    <strong class="filter-label-text">Поиск:</strong>
    <input class="filter-input search-input" type="text"
            name="search"
            :placeholder="placeholder"
            :value="search"
            onchange="this.form.submit()">
</div>
</template>

<style>
.filter-group {
    display: flex;
    align-items: center;
    gap: 10px;
    background: white;
    padding: 10px 15px;
    border-radius: 6px;
    border: 1px solid #ddd;
}

.filter-label-text {
    font-weight: 600;
    color: #333;
    white-space: nowrap;
}

/* Поля ввода */
.filter-input {
    padding: 8px 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 14px;
}

.search-input {
    min-width: 200px;
}

.filter-input:focus {
    outline: none;
    border-color: #ff8a00;
    box-shadow: 0 0 0 2px rgba(255, 138, 0, 0.1);
}
</style>