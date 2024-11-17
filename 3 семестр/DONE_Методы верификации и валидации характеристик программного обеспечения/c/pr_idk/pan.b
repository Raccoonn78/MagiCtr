	switch (t->back) {
	default: Uerror("bad return move");
	case  0: goto R999; /* nothing to undo */

		 /* PROC :init: */

	case 3: // STATE 1
		;
		;
		delproc(0, now._nr_pr-1);
		;
		goto R999;

	case 4: // STATE 2
		;
		p_restor(II);
		;
		;
		goto R999;

		 /* PROC GCD */

	case 5: // STATE 2
		;
		((P0 *)_this)->b = trpt->bup.ovals[1];
		((P0 *)_this)->a = trpt->bup.ovals[0];
		;
		ungrab_ints(trpt->bup.ovals, 2);
		goto R999;

	case 6: // STATE 6
		;
		((P0 *)_this)->a = trpt->bup.ovals[2];
		((P0 *)_this)->b = trpt->bup.ovals[1];
		((P0 *)_this)->temp = trpt->bup.ovals[0];
		;
		ungrab_ints(trpt->bup.ovals, 3);
		goto R999;

	case 7: // STATE 8
		;
		((P0 *)_this)->result = trpt->bup.ovals[1];
	/* 0 */	((P0 *)_this)->b = trpt->bup.ovals[0];
		;
		;
		ungrab_ints(trpt->bup.ovals, 2);
		goto R999;
;
		
	case 8: // STATE 13
		goto R999;

	case 9: // STATE 14
		;
		p_restor(II);
		;
		;
		goto R999;
	}

