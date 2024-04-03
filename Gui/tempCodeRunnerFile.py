def start_to_queue(self):
        self.output_text.clear()
        addQueue(self.rate_dict)
        self.rate_dict.clear()
        thread1=threading.Thread(target=startQueue)
        thread1.start()