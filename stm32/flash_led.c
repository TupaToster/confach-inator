#include "main.h"
#include "stm32f4xx_hal.h"

int main(void) {
  HAL_Init();
  SystemClock_Config();

  // Enable GPIOA Clock
  __HAL_RCC_GPIOA_CLK_ENABLE();

  // Configure PA5 (LED)
  GPIO_InitTypeDef GPIO_InitStruct = {0};
  GPIO_InitStruct.Pin = GPIO_PIN_5;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

  while (1) {
    HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);  // Toggle LED
    HAL_Delay(500);                         // 500ms delay
  }
}
