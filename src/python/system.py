from browser import window

def asTask(jsTask):
    while True:
        result = jsTask.next()
        if window.hasProperty(result, 'value'):
            yield result['value']
        if window.hasProperty(result, 'done') and result['done']:
            break

def main():
    _engine = window.Engine.new()
    task = asTask(window.mainTask(_engine))
    def taskFn():
        nonlocal task
        try:
            # TODO: May be able to use yielded generator as a goto.
            value = next(task)
        except StopIteration:
            return False
        else:
            return True
    _engine.run(taskFn)

if __name__ == '__main__':
    main()
