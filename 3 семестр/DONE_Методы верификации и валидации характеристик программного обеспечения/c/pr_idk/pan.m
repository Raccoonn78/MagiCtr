#define rand	pan_rand
#define pthread_equal(a,b)	((a)==(b))
#if defined(HAS_CODE) && defined(VERBOSE)
	#ifdef BFS_PAR
		bfs_printf("Pr: %d Tr: %d\n", II, t->forw);
	#else
		cpu_printf("Pr: %d Tr: %d\n", II, t->forw);
	#endif
#endif
	switch (t->forw) {
	default: Uerror("bad forward move");
	case 0:	/* if without executable clauses */
		continue;
	case 1: /* generic 'goto' or 'skip' */
		IfNotBlocked
		_m = 3; goto P999;
	case 2: /* generic 'else' */
		IfNotBlocked
		if (trpt->o_pm&1) continue;
		_m = 3; goto P999;

		 /* PROC :init: */
	case 3: // STATE 1 - gcd_model.pml:27 - [(run GCD())] (0:0:0 - 1)
		IfNotBlocked
		reached[1][1] = 1;
		if (!(addproc(II, 1, 0)))
			continue;
		_m = 3; goto P999; /* 0 */
	case 4: // STATE 2 - gcd_model.pml:28 - [-end-] (0:0:0 - 1)
		IfNotBlocked
		reached[1][2] = 1;
		if (!delproc(1, II)) continue;
		_m = 3; goto P999; /* 0 */

		 /* PROC GCD */
	case 5: // STATE 1 - gcd_model.pml:9 - [a = 48] (0:10:2 - 1)
		IfNotBlocked
		reached[0][1] = 1;
		(trpt+1)->bup.ovals = grab_ints(2);
		(trpt+1)->bup.ovals[0] = ((P0 *)_this)->a;
		((P0 *)_this)->a = 48;
#ifdef VAR_RANGES
		logval("GCD:a", ((P0 *)_this)->a);
#endif
		;
		/* merge: b = 18(10, 2, 10) */
		reached[0][2] = 1;
		(trpt+1)->bup.ovals[1] = ((P0 *)_this)->b;
		((P0 *)_this)->b = 18;
#ifdef VAR_RANGES
		logval("GCD:b", ((P0 *)_this)->b);
#endif
		;
		/* merge: .(goto)(0, 11, 10) */
		reached[0][11] = 1;
		;
		_m = 3; goto P999; /* 2 */
	case 6: // STATE 3 - gcd_model.pml:13 - [((b!=0))] (10:0:3 - 1)
		IfNotBlocked
		reached[0][3] = 1;
		if (!((((P0 *)_this)->b!=0)))
			continue;
		/* merge: temp = b(10, 4, 10) */
		reached[0][4] = 1;
		(trpt+1)->bup.ovals = grab_ints(3);
		(trpt+1)->bup.ovals[0] = ((P0 *)_this)->temp;
		((P0 *)_this)->temp = ((P0 *)_this)->b;
#ifdef VAR_RANGES
		logval("GCD:temp", ((P0 *)_this)->temp);
#endif
		;
		/* merge: b = (a%b)(10, 5, 10) */
		reached[0][5] = 1;
		(trpt+1)->bup.ovals[1] = ((P0 *)_this)->b;
		((P0 *)_this)->b = (((P0 *)_this)->a%((P0 *)_this)->b);
#ifdef VAR_RANGES
		logval("GCD:b", ((P0 *)_this)->b);
#endif
		;
		/* merge: a = temp(10, 6, 10) */
		reached[0][6] = 1;
		(trpt+1)->bup.ovals[2] = ((P0 *)_this)->a;
		((P0 *)_this)->a = ((P0 *)_this)->temp;
#ifdef VAR_RANGES
		logval("GCD:a", ((P0 *)_this)->a);
#endif
		;
		/* merge: .(goto)(0, 11, 10) */
		reached[0][11] = 1;
		;
		_m = 3; goto P999; /* 4 */
	case 7: // STATE 7 - gcd_model.pml:17 - [((b==0))] (14:0:2 - 1)
		IfNotBlocked
		reached[0][7] = 1;
		if (!((((P0 *)_this)->b==0)))
			continue;
		if (TstOnly) return 1; /* TT */
		/* dead 1: b */  (trpt+1)->bup.ovals = grab_ints(2);
		(trpt+1)->bup.ovals[0] = ((P0 *)_this)->b;
#ifdef HAS_CODE
		if (!readtrail)
#endif
			((P0 *)_this)->b = 0;
		/* merge: result = a(14, 8, 14) */
		reached[0][8] = 1;
		(trpt+1)->bup.ovals[1] = ((P0 *)_this)->result;
		((P0 *)_this)->result = ((P0 *)_this)->a;
#ifdef VAR_RANGES
		logval("GCD:result", ((P0 *)_this)->result);
#endif
		;
		/* merge: goto :b0(14, 9, 14) */
		reached[0][9] = 1;
		;
		/* merge: printf('НОД равен %d\\n',result)(14, 13, 14) */
		reached[0][13] = 1;
		Printf("НОД равен %d\n", ((P0 *)_this)->result);
		_m = 3; goto P999; /* 3 */
	case 8: // STATE 13 - gcd_model.pml:23 - [printf('НОД равен %d\\n',result)] (0:14:0 - 3)
		IfNotBlocked
		reached[0][13] = 1;
		Printf("НОД равен %d\n", ((P0 *)_this)->result);
		_m = 3; goto P999; /* 0 */
	case 9: // STATE 14 - gcd_model.pml:24 - [-end-] (0:0:0 - 1)
		IfNotBlocked
		reached[0][14] = 1;
		if (!delproc(1, II)) continue;
		_m = 3; goto P999; /* 0 */
	case  _T5:	/* np_ */
		if (!((!(trpt->o_pm&4) && !(trpt->tau&128))))
			continue;
		/* else fall through */
	case  _T2:	/* true */
		_m = 3; goto P999;
#undef rand
	}

