<script setup>
defineProps({
  label: {
    type: String,
    required: true
  },
  name: {
    type: String,
    required: true
  },
  emptyLabel: {
    type: String,
    required: true
  },
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
    <strong class="filter-label-text">{{ label }}:</strong>
    <label class="filter-radio-label">
        <input class="filter-radio" type="radio" :name="name" value=""
                :checked="!currentFilter"
                onchange="this.form.submit()">
        <span class="filter-radio-text">{{ emptyLabel }}</span>
    </label>
    <label v-for="item in items" class="filter-radio-label">
        <input class="filter-radio" type="radio" :name="name" :value="item"
                :checked="currentFilter === item"
                onchange="this.form.submit()">
        <span class="filter-radio-text">{{ item }}</span>
    </label>
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

.filter-radio-label {
    display: flex;
    align-items: center;
    gap: 5px;
    cursor: pointer;
    padding: 4px 8px;
    border-radius: 4px;
    transition: background-color 0.2s;
}

.filter-radio-label:hover {
    background-color: #f0f0f0;
}

.filter-radio {
    margin: 0;
}

.filter-radio-text {
    font-size: 14px;
    color: #666;
}

.filter-radio:checked + .filter-radio-text {
    color: #ff8a00;
    font-weight: 500;
}
</style>