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
    <strong class="filter-label-text">{{ label }}</strong>
    <select :value="currentFilter" class="filter-select" :name="name" onchange="this.form.submit()">
        <option key="" value="">{{ emptyLabel }}</option>
        <option v-for="item in items" :key="item" :value="item">{{ item }}</option>
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
    font-size: 0.5em;
    background: white;
    min-width: 120px;
}

.filter-select:focus {
    outline: none;
    border-color: #ff8a00;
}

@media (max-width: 820px) {
  .filter-label-text {
    font-size: 14px;
  }
  .filter-select {
    font-size: 14px !important;
  }
  .filter-input {
    font-size: 14px;
  }
  .filter-radio-text {
    font-size: 14px;
  }
  .clear-button {
    font-size: 0.5em;
  }
}
</style>