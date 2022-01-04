/*
 * Namespaces.h
 *
 *  Created on: 04.01.2022
 *      Author: kutz
 */

#ifndef NAMESPACES_H_
#define NAMESPACES_H_

namespace NSP {

	namespace Inner {

		class Namespaced {
		public:
			Namespaced();
			virtual ~Namespaced();
		};
	}
}

#endif /* NAMESPACES_H_ */
