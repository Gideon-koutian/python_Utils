# -*- coding: utf-8 -*-
import faker

fake = faker.Faker(locale=['zh_cn', 'en-US'])


def main():
    print(responsible(), online_user())


def responsible():
    return {
        'name': fake.name(),
        'tel': fake.phone_number(),
        'email': fake.company_email()
    }


def online_user():
    # network:网段模式
    network = False
    return {
        'ipv4': fake.ipv4_private(network=network),
        'ipv6': fake.ipv6(network=network),
        'mac': fake.mac_address(),
        'user': fake.user_name()
    }


if __name__ == '__main__':
    main()
