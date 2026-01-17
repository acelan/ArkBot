import pytest
import asyncio
import os
from arkbrain import ArkBrain

@pytest.mark.asyncio
async def test_full_conversation_flow():
    if not os.getenv('GOOGLE_GENAI_API_KEY'):
        pytest.skip("GOOGLE_GENAI_API_KEY not set")

    brain = ArkBrain()

    response1 = await brain.thinking('test_thread', '請分析 AAPL 這支股票')
    assert len(response1) > 0
    assert 'AAPL' in response1 or '蘋果' in response1

    response2 = await brain.thinking('test_thread', '那它的股息如何？')
    assert len(response2) > 0

@pytest.mark.asyncio
async def test_taiwan_stock():
    if not os.getenv('GOOGLE_GENAI_API_KEY'):
        pytest.skip("GOOGLE_GENAI_API_KEY not set")

    brain = ArkBrain()
    response = await brain.thinking('test_tw', '請告訴我 2330.TW 的基本資訊')
    assert len(response) > 0

@pytest.mark.asyncio
async def test_multiple_threads():
    if not os.getenv('GOOGLE_GENAI_API_KEY'):
        pytest.skip("GOOGLE_GENAI_API_KEY not set")

    brain = ArkBrain()

    response1 = await brain.thinking('thread1', '分析 AAPL')
    response2 = await brain.thinking('thread2', '分析 TSLA')

    assert 'AAPL' in response1 or '蘋果' in response1
    assert 'TSLA' in response2 or '特斯拉' in response2
