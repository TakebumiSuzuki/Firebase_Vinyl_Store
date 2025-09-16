<!--
  通常の <script> ブロック
  ここに書かれた変数は、コンポーネントの外部（モジュールスコープ）で定義されます。
-->
<script>
  const colorVariants = {
    emerald: {
      border: 'hover:border-emerald-400/50',
      ring: 'focus:ring-emerald-400/20',
      gradientFrom: 'from-emerald-500/10',
      gradientTo: 'to-teal-500/10',
      text: 'group-hover:text-emerald-100',
      icon: 'group-hover:text-emerald-400',
    },
    purple: {
      border: 'hover:border-purple-400/50',
      ring: 'focus:ring-purple-400/20',
      gradientFrom: 'from-purple-500/10',
      gradientTo: 'to-violet-500/10',
      text: 'group-hover:text-purple-100',
      icon: 'group-hover:text-purple-400',
    },
    teal: {
      border: 'hover:border-teal-400/50',
      ring: 'focus:ring-teal-400/20',
      gradientFrom: 'from-teal-500/10',
      gradientTo: 'to-cyan-500/10',
      text: 'group-hover:text-teal-100',
      icon: 'group-hover:text-teal-400',
    },
    red: {
      border: 'hover:border-red-400/50',
      ring: 'focus:ring-red-400/20',
      gradientFrom: 'from-red-500/10',
      gradientTo: 'to-pink-500/10',
      text: 'group-hover:text-red-100',
      icon: 'group-hover:text-red-400',
    },
    // 他の色を追加する場合はここに追記
  };
</script>

<!--
  <script setup> ブロック
  コンポーネントのリアクティブなロジックを記述します。
-->
<script setup>
  import { computed } from 'vue'

  const props = defineProps({
    baseColor: {
      type: String,
      required: true,
      // この validator は、上の<script>で定義された colorVariants を参照できるため、エラーになりません。
      validator: (value) => Object.keys(colorVariants).includes(value),
    },
    buttonTitle: {
      type: String,
      required: true,
    },
  })

  // props.baseColor に応じて、対応する色のクラスセットを取得
  const selectedColorSet = computed(() => colorVariants[props.baseColor])

  // 各パーツに適用する動的なクラス
  const rootClasses = computed(() => [
    selectedColorSet.value.border,
    selectedColorSet.value.ring,
  ])

  const gradientClasses = computed(() => [
    selectedColorSet.value.gradientFrom,
    selectedColorSet.value.gradientTo,
  ])

  const textClasses = computed(() => [
    selectedColorSet.value.text,
  ])

  const iconWrapperClasses = computed(() => [
    'w-5', 'h-5',
    'transition-all', 'duration-300',
    'group-hover:scale-110',
    selectedColorSet.value.icon,
  ])
</script>

<template>
  <div
    :class="rootClasses"
    class="group relative overflow-hidden bg-neutral-800 hover:bg-neutral-700 text-white font-semibold py-4 px-6 rounded-xl transition-all duration-300 transform hover:scale-[1.02] hover:shadow-xl border border-neutral-700 focus:outline-none focus:ring-4 active:scale-[0.98]"
  >
    <div
      :class="gradientClasses"
      class="absolute inset-0 bg-gradient-to-r opacity-0 group-hover:opacity-100 transition-opacity duration-300"
    ></div>

    <span
      :class="textClasses"
      class="relative flex items-center justify-center gap-2 transition-colors duration-300"
    >
      <span :class="iconWrapperClasses">
        <slot />
      </span>

      {{ buttonTitle }}
    </span>
  </div>
</template>