/*
 * SSTF IO Scheduler - Implemented by Carlos Moratelli
 *
 * For Kernel 4.12.4
 *
 */
#include <linux/blkdev.h>
#include <linux/elevator.h>
#include <linux/bio.h>
#include <linux/module.h>
#include <linux/slab.h>
#include <linux/init.h>

/* SSTF data structure. */
struct sstf_data {
	struct list_head queue;
};

int currentPosition = 0;

/* Esta função despacha o próximo bloco a ser lido. */
static int sstf_dispatch(struct request_queue *q, int force){

    //printk("starting dispatch process");
	struct sstf_data *nd = q->elevator->elevator_data;
	char direction = 'R';
	struct request *rq = NULL;

	// MARK: Remove from list
	//blk_rq_pos -> position block
	int currentDifference = 9999999;
	struct list_head *pointer = NULL;
	struct request *toRemove = NULL;

    if(list_empty(&nd->queue)){
        //printk("List empty");
        return 0;
    }

	list_for_each(pointer, &nd->queue) {
        rq = list_entry(pointer, struct request, queuelist);
		int difference = abs(blk_rq_pos(rq) - currentPosition);
		if (difference < currentDifference) {
			currentDifference = difference;
			toRemove = rq;
		}
	}


     currentPosition = blk_rq_pos(toRemove);
	 list_del_init(&toRemove->queuelist);
	 elv_dispatch_sort(q, toRemove);

     if (rq_data_dir(toRemove) == READ) {
         direction = 'R';
     } else {
         direction = 'W';
     }
     printk(KERN_EMERG "[SSTF] dsp %c %lu\n", direction, blk_rq_pos(toRemove));
	 return 1;

}

static void sstf_add_request(struct request_queue *q, struct request *rq){
    //printk("starting add process");
	struct sstf_data *nd = q->elevator->elevator_data;
	char direction = 'R';

	// MARK: Add on list
	//adding at the end of the list
    list_add_tail(&rq->queuelist, &nd->queue);
    if (rq_data_dir(rq) == READ) {
        direction = 'R';
    } else {
        direction = 'W';
    } 
	printk(KERN_EMERG "[SSTF] add %c %lu\n", direction, blk_rq_pos(rq));


}


static int sstf_init_queue(struct request_queue *q, struct elevator_type *e){
	struct sstf_data *nd;
	struct elevator_queue *eq;

	/* Implementação da inicialização da fila (queue).
	 *
	 * Use como exemplo a inicialização da fila no driver noop-iosched.c
	 *
	 */

	eq = elevator_alloc(q, e);
	if (!eq)
		return -ENOMEM;

	nd = kmalloc_node(sizeof(*nd), GFP_KERNEL, q->node);
	if (!nd) {
		kobject_put(&eq->kobj);
		return -ENOMEM;
	}
	eq->elevator_data = nd;

	INIT_LIST_HEAD(&nd->queue);

	spin_lock_irq(q->queue_lock);
	q->elevator = eq;
	spin_unlock_irq(q->queue_lock);
	return 0;
}

static void sstf_exit_queue(struct elevator_queue *e){
	struct sstf_data *nd = e->elevator_data;

	/* Implementação da finalização da fila (queue).
	 *
	 * Use como exemplo o driver noop-iosched.c
	 *
	 */

	BUG_ON(!list_empty(&nd->queue));
	kfree(nd);

}

/* Infrastrutura dos drivers de IO Scheduling. */
static struct elevator_type elevator_sstf = {
	.ops.sq = {
		.elevator_dispatch_fn		= sstf_dispatch,
		.elevator_add_req_fn		= sstf_add_request,
		.elevator_init_fn		= sstf_init_queue,
		.elevator_exit_fn		= sstf_exit_queue,
	},
	.elevator_name = "sstf",
	.elevator_owner = THIS_MODULE,
};

/* Inicialização do driver. */
static int __init sstf_init(void){
	elv_register(&elevator_sstf);

	return 0;
}

/* Finalização do driver. */
static void __exit sstf_exit(void){
	elv_unregister(&elevator_sstf);
}

module_init(sstf_init);
module_exit(sstf_exit);


MODULE_AUTHOR("Barbara Kudiess");
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("SSTF IO scheduler");
