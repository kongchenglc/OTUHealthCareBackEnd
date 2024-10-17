import { pipeline } from '@xenova/transformers';
import Router from 'koa-router';
const router = new Router();

router.prefix('/gptchat')

router.get('/', async function (ctx, next) {
  const userInput = ctx.query.message
  const model = await pipeline('text-generation', 'onnx-community/Llama-3.2-1B-Instruct-q4f16');
  const response = await model(userInput || 'Input Nothing');
  ctx.body = response?.[0]?.generated_text
})

export default router
