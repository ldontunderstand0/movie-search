<script setup>
defineProps({
  currentFilter: {
    type: String,
    required: true
  },
  items: {
    type: [Array, Object],
    default: () => [],
    required: true
  },
})
</script>

<template>
<div class="filter-group">
    <strong class="filter-label-text">Сортировка</strong>
    <select :value="currentFilter" class="filter-select" name="sort" onchange="this.form.submit()">
        <option key="" value="">По умолчанию</option>
        <option v-for="item in items" :key="item.filter" :value="item.filter">{{ item.label }}</option>
    </select>
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

.filter-select {
    padding: 8px 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 14px;
    background: white;
    min-width: 120px;
}

.filter-select:focus {
    outline: none;
    border-color: #ff8a00;
}
</style>