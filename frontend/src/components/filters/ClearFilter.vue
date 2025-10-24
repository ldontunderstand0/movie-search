<template>
<div class="filter-group">
    <a href="?" class="filter-button clear-button">Сбросить</a>
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
.filter-button {
    display: inline-block;
    padding: 8px 16px;
    border-radius: 4px;
    text-decoration: none;
    font-size: 1em;
    font-weight: 500;
    transition: all 0.3s ease;
}

.clear-button {
    background: #ff8a00;
    color: white;
}

.clear-button:hover {
    background: #e67a00;
    transform: translateY(-1px);
}
</style>