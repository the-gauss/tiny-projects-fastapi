import asyncio

async def async_function(test_param: str) -> str:
    print('This is async func')
    await asyncio.sleep(4)  # When this await is encountered, it yields control back to the event loop
    return f'Async Result: {test_param}'

# async def main():
#     print('Start of main')
#     task1 = async_function("Test 1")
#     task2 = async_function("Test 2")
#     print('End of main')

#     task1_result = await task1 # pauses execution of main until coroutine func finishes
#     task2_result = await task2 # pauses execution of main until coroutine func finishes
#     print(task1_result)
#     print(task2_result)

# Tasks
async def main():
    task1 = asyncio.create_task(async_function("Test 1"))
    task2 = asyncio.create_task(async_function("Test 2"))

    task1_result = await task1 # pauses execution of main until coroutine func finishes
    task2_result = await task2 # pauses execution of main until coroutine func finishes
    print(task1_result)
    print(task2_result)

if __name__ == "__main__":
    asyncio.run(main())